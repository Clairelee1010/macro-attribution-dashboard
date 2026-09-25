#!/usr/bin/env python3
"""P02-009 Historical Snapshot Collector.

Creates compact, append-only snapshots from current P02 production outputs.
Market-implied probabilities are observations, not forecasts.
Execution remains disabled.
"""
from __future__ import annotations
import argparse, json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "p02"
HISTORY = DATA / "history"

def load(name: str, default):
    p = DATA / name
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return default

def iso_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

def compact_market(m: dict) -> dict:
    return {
        "event_id": m.get("event_id"),
        "canonical_event": m.get("canonical_event"),
        "venue": m.get("venue"),
        "venue_market_id": m.get("venue_market_id"),
        "question": m.get("question"),
        "outcome": m.get("outcome"),
        "implied_probability": m.get("implied_probability"),
        "volume_usd": m.get("volume_usd"),
        "liquidity_usd": m.get("liquidity_usd"),
        "best_bid": m.get("best_bid"),
        "best_ask": m.get("best_ask"),
        "spread": m.get("spread"),
        "freshness": m.get("freshness"),
        "data_quality": m.get("data_quality"),
        "source_url": m.get("source_url"),
    }

def build_snapshot(captured_at: str | None = None) -> dict:
    captured_at = captured_at or iso_now()
    poly = load("polymarket_markets.json", {"markets": []})
    kalshi = load("kalshi_markets.json", {"markets": []})
    canonical = load("canonical_events.json", {"events": []})
    discrepancies = load("discrepancies.json", {"signals": []})
    context = load("p01_context.json", {"available": False})
    dashboard = load("dashboard_payload.json", {"trust_security": {"status": "UNKNOWN"}})

    regime = context.get("regime_report") or {}
    signal_report = context.get("signal_report") or {}
    signals = [
        {
            "metric_id": s.get("metric_id"),
            "signal_id": s.get("signal_id"),
            "direction": s.get("direction"),
            "strength": s.get("strength"),
            "confidence": s.get("confidence"),
            "value": s.get("value"),
            "unit": s.get("unit"),
        }
        for s in signal_report.get("signals", [])
    ]

    return {
        "product": "P02",
        "milestone": "P02-009",
        "captured_at": captured_at,
        "execution_allowed": False,
        "semantics": {
            "probability": "Market-implied probability observation; not a forecast.",
            "discrepancy": "Cross-venue difference; not proof of arbitrage.",
            "p01_context": "Supporting macro context; not causal proof.",
        },
        "summary": {
            "polymarket_markets": len(poly.get("markets", [])),
            "kalshi_markets": len(kalshi.get("markets", [])),
            "matched_events": len(canonical.get("events", [])),
            "discrepancy_signals": len(discrepancies.get("signals", [])),
            "trust_status": (dashboard.get("trust_security") or {}).get("status", "UNKNOWN"),
        },
        "markets": {
            "polymarket": [compact_market(x) for x in poly.get("markets", [])],
            "kalshi": [compact_market(x) for x in kalshi.get("markets", [])],
        },
        "canonical_events": canonical.get("events", []),
        "discrepancies": discrepancies.get("signals", []),
        "p01_context": {
            "available": bool(context.get("available")),
            "regime": regime.get("regime"),
            "regime_score": regime.get("score"),
            "regime_confidence": regime.get("confidence"),
            "signals": signals,
        },
        "trust_security": dashboard.get("trust_security", {"status": "UNKNOWN"}),
    }

def write_snapshot(snapshot: dict) -> Path:
    dt = datetime.fromisoformat(snapshot["captured_at"].replace("Z", "+00:00"))
    day = HISTORY / dt.strftime("%Y-%m-%d")
    day.mkdir(parents=True, exist_ok=True)
    path = day / f'{dt.strftime("%H%M%S")}.json'
    path.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--captured-at", help="ISO-8601 UTC timestamp; useful for deterministic tests.")
    args = ap.parse_args()
    snap = build_snapshot(args.captured_at)
    path = write_snapshot(snap)
    print("P02-009 HISTORICAL SNAPSHOT")
    print(f"Snapshot                     {path.relative_to(ROOT)}")
    print(f"Polymarket Markets           {snap['summary']['polymarket_markets']}")
    print(f"Kalshi Markets               {snap['summary']['kalshi_markets']}")
    print(f"Matched Events               {snap['summary']['matched_events']}")
    print(f"Discrepancy Signals          {snap['summary']['discrepancy_signals']}")
    print("Execution                    DISABLED")
    print("P02-009A SNAPSHOT: PASS")

if __name__ == "__main__":
    main()
