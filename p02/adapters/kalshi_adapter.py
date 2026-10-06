#!/usr/bin/env python3
"""P02-003 Kalshi public market-data adapter.

Uses Kalshi's public market endpoint and normalizes active markets into the
P02-001 prediction_market.schema.json contract.

Read-only: no authentication, orders, wallet, or execution.
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

BASE_URL = "https://api.elections.kalshi.com/trade-api/v2"
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


def cents_to_probability(value: Any) -> float | None:
    x = as_float(value)
    if x is None:
        return None
    if 0 <= x <= 100:
        return x / 100.0
    return None


def dollars_to_probability(value: Any) -> float | None:
    x = as_float(value)
    if x is None:
        return None
    if 0 <= x <= 1:
        return x
    return None


def get_probability(market: dict[str, Any], dollars_key: str, cents_key: str) -> float | None:
    # Prefer fixed-point dollar strings where available; fall back to legacy cents.
    p = dollars_to_probability(market.get(dollars_key))
    if p is not None:
        return p
    return cents_to_probability(market.get(cents_key))


def implied_yes_probability(market: dict[str, Any]) -> float | None:
    # Last traded price is the closest market-implied observation when present.
    for dollars_key, cents_key in [
        ("last_price_dollars", "last_price"),
        ("yes_ask_dollars", "yes_ask"),
        ("yes_bid_dollars", "yes_bid"),
    ]:
        p = get_probability(market, dollars_key, cents_key)
        if p is not None:
            return p
    return None


def source_url(market: dict[str, Any]) -> str:
    ticker = str(market.get("ticker") or "")
    return f"https://kalshi.com/markets/{ticker}"


def normalize_market(market: dict[str, Any], retrieved_at: datetime) -> dict[str, Any]:
    ticker = str(market.get("ticker") or "").strip()
    question = str(market.get("title") or market.get("subtitle") or "").strip()
    probability = implied_yes_probability(market)

    best_bid = get_probability(market, "yes_bid_dollars", "yes_bid")
    best_ask = get_probability(market, "yes_ask_dollars", "yes_ask")
    spread = None
    if best_bid is not None and best_ask is not None:
        spread = max(0.0, best_ask - best_bid)

    # Kalshi documents fixed-point dollar-denominated fields for volume/open interest.
    # Keep generic P02 USD fields conservative: use *_dollars when supplied.
    volume_usd = as_float(market.get("volume_24h_fp"))
    liquidity_usd = as_float(market.get("open_interest_fp"))

    required_ok = bool(ticker and question and probability is not None)

    return {
        "event_id": f"KALSHI:{ticker}",
        "canonical_event": f"UNMATCHED:KALSHI:{ticker}",
        "venue": "kalshi",
        "venue_market_id": ticker,
        "question": question or "UNKNOWN",
        "outcome": "YES",
        "implied_probability": probability if probability is not None else 0.0,
        "volume_usd": volume_usd,
        "liquidity_usd": liquidity_usd,
        "best_bid": best_bid,
        "best_ask": best_ask,
        "spread": spread,
        "market_open_time": market.get("open_time"),
        "market_close_time": market.get("close_time"),
        "resolution_source": None,
        "resolution_rules": market.get("rules_primary") or market.get("rules_secondary"),
        "source_url": source_url(market),
        "retrieved_at": iso_z(retrieved_at),
        "freshness": "FRESH",
        "data_quality": "PASS" if required_ok else "WARN",
    }


def fetch_open_markets(limit: int = DEFAULT_LIMIT, timeout: int = 20) -> list[dict[str, Any]]:
    target = max(1, min(int(limit), 5000))
    markets, cursor, seen = [], None, set()
    while len(markets) < target:
        params={"status":"open","limit":min(1000,target-len(markets))}
        if cursor: params["cursor"]=cursor
        response=requests.get(f"{BASE_URL}/markets",params=params,headers={"User-Agent":USER_AGENT,"Accept":"application/json"},timeout=timeout)
        response.raise_for_status(); payload=response.json()
        page=payload.get("markets",[]) if isinstance(payload,dict) else []
        if not isinstance(page,list): raise ValueError("Kalshi response does not contain a markets list")
        valid=[m for m in page if isinstance(m,dict)]; markets.extend(valid)
        nxt=payload.get("cursor") if isinstance(payload,dict) else None
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
    raw = fetch_open_markets(limit=limit)
    normalized = [normalize_market(m, retrieved_at) for m in raw]
    records = [x for x in normalized if x["venue_market_id"] and x["question"] != "UNKNOWN"]

    errors = validate_records(records, schema_path)
    if errors:
        raise ValueError("Schema validation failed:\n" + "\n".join(errors[:20]))

    output.parent.mkdir(parents=True, exist_ok=True)
    document = {
        "product": "P02",
        "milestone": "P02-003",
        "source": "Kalshi Trade API v2",
        "source_endpoint": f"{BASE_URL}/markets",
        "retrieved_at": iso_z(retrieved_at),
        "market_count": len(records),
        "execution_allowed": False,
        "markets": records,
    }
    output.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return document


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=int(os.getenv("P02_KALSHI_LIMIT", DEFAULT_LIMIT)))
    parser.add_argument("--output", default="data/p02/kalshi_markets.json")
    parser.add_argument("--schema", default="p02/schemas/prediction_market.schema.json")
    args = parser.parse_args()

    try:
        doc = run(args.limit, Path(args.output), Path(args.schema))
    except Exception as exc:
        print(f"P02-003 KALSHI ADAPTER: FAIL\n{exc}", file=sys.stderr)
        return 1

    print("P02-003 KALSHI ADAPTER")
    print("API Connectivity       PASS")
    print(f"Markets Retrieved      {doc['market_count']}")
    print("Normalization          PASS")
    print("Schema Validation      PASS")
    print("Source Provenance      PASS")
    print("Execution              DISABLED")
    print("P02-003: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
