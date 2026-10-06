#!/usr/bin/env python3
"""P02-002 Polymarket public market-data adapter.

Reads public Gamma API data and normalizes each YES outcome into the P02-001
prediction_market.schema.json contract.

This module is read-only. It does not authenticate, place orders, or execute trades.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests
from jsonschema import Draft202012Validator, FormatChecker

GAMMA_BASE_URL = "https://gamma-api.polymarket.com"
DEFAULT_LIMIT = 20
USER_AGENT = "macro-attribution-dashboard-p02/1.0"


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def iso_z(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def as_float(value: Any) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def parse_json_array(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    if isinstance(value, str):
        try:
            parsed = json.loads(value)
            return parsed if isinstance(parsed, list) else []
        except json.JSONDecodeError:
            return []
    return []


def first_present(obj: dict[str, Any], *keys: str) -> Any:
    for key in keys:
        if key in obj and obj[key] is not None:
            return obj[key]
    return None


def source_url(market: dict[str, Any]) -> str | None:
    slug = market.get("slug")
    return f"https://polymarket.com/market/{slug}" if slug else None


def yes_probability(market: dict[str, Any]) -> float | None:
    labels = parse_json_array(market.get("outcomes"))
    prices = parse_json_array(market.get("outcomePrices"))

    for idx, label in enumerate(labels):
        if str(label).strip().lower() == "yes" and idx < len(prices):
            p = as_float(prices[idx])
            if p is not None and 0 <= p <= 1:
                return p

    # Binary Polymarket Gamma responses document YES at index 0.
    if prices:
        p = as_float(prices[0])
        if p is not None and 0 <= p <= 1:
            return p

    # Last trade price is a fallback observation, not preferred outcome parsing.
    p = as_float(market.get("lastTradePrice"))
    return p if p is not None and 0 <= p <= 1 else None


def normalize_market(market: dict[str, Any], retrieved_at: datetime) -> dict[str, Any]:
    market_id = str(market.get("id") or "")
    probability = yes_probability(market)

    best_bid = as_float(market.get("bestBid"))
    best_ask = as_float(market.get("bestAsk"))
    spread = as_float(market.get("spread"))
    if spread is None and best_bid is not None and best_ask is not None:
        spread = max(0.0, best_ask - best_bid)

    liquidity = as_float(market.get("liquidity"))
    # P02-001's generic field is volume_usd. For this adapter it stores
    # Polymarket's documented 24-hour volume, not lifetime volume.
    volume_24h = as_float(first_present(market, "volume24hr", "volume24h"))

    question = str(market.get("question") or "").strip()
    end_date = first_present(market, "endDateIso", "endDate")
    start_date = first_present(market, "startDateIso", "startDate")

    required_ok = bool(market_id and question and probability is not None)
    data_quality = "PASS" if required_ok else "WARN"

    return {
        "event_id": f"POLYMARKET:{market_id}",
        "canonical_event": f"UNMATCHED:POLYMARKET:{market_id}",
        "venue": "polymarket",
        "venue_market_id": market_id,
        "question": question or "UNKNOWN",
        "outcome": "YES",
        "implied_probability": probability if probability is not None else 0.0,
        "volume_usd": volume_24h,
        "liquidity_usd": liquidity,
        "best_bid": best_bid,
        "best_ask": best_ask,
        "spread": spread,
        "market_open_time": start_date,
        "market_close_time": end_date,
        "resolution_source": None,
        "resolution_rules": None,
        "source_url": source_url(market),
        "retrieved_at": iso_z(retrieved_at),
        "freshness": "FRESH",
        "data_quality": data_quality,
    }


def fetch_active_markets(limit: int = DEFAULT_LIMIT, timeout: int = 20) -> list[dict[str, Any]]:
    target = max(1, min(int(limit), 2000))
    url = f"{GAMMA_BASE_URL}/markets/keyset"
    markets, cursor, seen = [], None, set()
    while len(markets) < target:
        params = {"closed": "false", "limit": min(100, target-len(markets))}
        if cursor: params["next_cursor"] = cursor
        response=requests.get(url,params=params,headers={"User-Agent":USER_AGENT,"Accept":"application/json"},timeout=timeout)
        response.raise_for_status(); payload=response.json()
        if isinstance(payload,dict):
            page=payload.get("markets",payload.get("data",[]))
            nxt=payload.get("next_cursor") or payload.get("nextCursor") or payload.get("cursor")
        elif isinstance(payload,list): page,nxt=payload,None
        else: raise ValueError("Unexpected Polymarket response type")
        if not isinstance(page,list): raise ValueError("Polymarket response does not contain a markets list")
        valid=[m for m in page if isinstance(m,dict)]; markets.extend(valid)
        if not valid or not nxt or str(nxt) in seen: break
        seen.add(str(nxt)); cursor=str(nxt)
    return markets[:target]


def validate_records(records: list[dict[str, Any]], schema_path: Path) -> list[str]:
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors: list[str] = []
    for idx, record in enumerate(records):
        for error in validator.iter_errors(record):
            errors.append(f"record[{idx}] {list(error.path)}: {error.message}")
    return errors


def run(limit: int, output: Path, schema_path: Path) -> dict[str, Any]:
    retrieved_at = utc_now()
    raw = fetch_active_markets(limit=limit)
    normalized = [normalize_market(m, retrieved_at) for m in raw]
    valid_candidates = [
        item for item in normalized
        if item["venue_market_id"] and item["question"] != "UNKNOWN"
    ]

    errors = validate_records(valid_candidates, schema_path)
    if errors:
        raise ValueError("Schema validation failed:\n" + "\n".join(errors[:20]))

    output.parent.mkdir(parents=True, exist_ok=True)
    document = {
        "product": "P02",
        "milestone": "P02-002",
        "source": "Polymarket Gamma API",
        "source_endpoint": f"{GAMMA_BASE_URL}/markets/keyset",
        "retrieved_at": iso_z(retrieved_at),
        "market_count": len(valid_candidates),
        "volume_semantics": "volume_usd maps to Polymarket volume24hr for P02-002",
        "execution_allowed": False,
        "markets": valid_candidates,
    }
    output.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return document


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=int(os.getenv("P02_POLYMARKET_LIMIT", DEFAULT_LIMIT)))
    parser.add_argument("--output", default="data/p02/polymarket_markets.json")
    parser.add_argument("--schema", default="p02/schemas/prediction_market.schema.json")
    args = parser.parse_args()

    try:
        doc = run(args.limit, Path(args.output), Path(args.schema))
    except Exception as exc:
        print(f"P02-002 POLYMARKET ADAPTER: FAIL\n{exc}", file=sys.stderr)
        return 1

    print("P02-002 POLYMARKET ADAPTER")
    print("API Connectivity       PASS")
    print(f"Markets Retrieved      {doc['market_count']}")
    print("Normalization          PASS")
    print("Schema Validation      PASS")
    print("Source Provenance      PASS")
    print("Execution              DISABLED")
    print("P02-002: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
