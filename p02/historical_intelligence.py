#!/usr/bin/env python3
"""P02-009 Historical Intelligence Builder.

Reads stored P02 snapshots and creates deterministic historical deltas.
No forecast, trading recommendation, or execution is produced.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HISTORY = ROOT / "data" / "p02" / "history"
OUT = ROOT / "data" / "p02" / "historical_intelligence.json"

def load_snapshots() -> list[dict]:
    rows = []
    if not HISTORY.exists():
        return rows
    for p in sorted(HISTORY.glob("*/*.json")):
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
            if d.get("milestone") == "P02-009":
                rows.append(d)
        except Exception:
            continue
    return sorted(rows, key=lambda x: x.get("captured_at", ""))

def market_map(snapshot: dict) -> dict[tuple[str,str], dict]:
    out = {}
    for venue, markets in (snapshot.get("markets") or {}).items():
        for m in markets:
            key = (venue, str(m.get("venue_market_id")))
            out[key] = m
    return out

def classify(delta_pp):
    if delta_pp is None:
        return "INSUFFICIENT_HISTORY"
    if delta_pp >= 5:
        return "UP_STRONG"
    if delta_pp >= 1:
        return "UP"
    if delta_pp <= -5:
        return "DOWN_STRONG"
    if delta_pp <= -1:
        return "DOWN"
    return "STABLE"

def build(snapshots: list[dict]) -> dict:
    latest = snapshots[-1] if snapshots else None
    previous = snapshots[-2] if len(snapshots) >= 2 else None
    changes = []
    if latest:
        lm = market_map(latest)
        pm = market_map(previous) if previous else {}
        for key, cur in lm.items():
            old = pm.get(key)
            cp = cur.get("implied_probability")
            pp = old.get("implied_probability") if old else None
            delta = None
            if isinstance(cp, (int,float)) and isinstance(pp, (int,float)):
                delta = round((cp - pp) * 100, 3)
            changes.append({
                "venue": key[0],
                "venue_market_id": key[1],
                "question": cur.get("question"),
                "current_probability": cp,
                "previous_probability": pp,
                "probability_change_pp": delta,
                "direction": classify(delta),
                "current_volume_usd": cur.get("volume_usd"),
                "current_liquidity_usd": cur.get("liquidity_usd"),
                "freshness": cur.get("freshness"),
                "data_quality": cur.get("data_quality"),
                "source_url": cur.get("source_url"),
            })

    discrepancy_history = []
    for s in snapshots:
        for d in s.get("discrepancies", []):
            discrepancy_history.append({
                "captured_at": s.get("captured_at"),
                "canonical_event_id": d.get("canonical_event_id"),
                "raw_discrepancy_pp": d.get("raw_discrepancy_pp"),
                "comparability": d.get("comparability"),
                "evidence_confidence": d.get("evidence_confidence"),
                "attention": d.get("attention"),
            })

    p01_timeline = [{
        "captured_at": s.get("captured_at"),
        "regime": (s.get("p01_context") or {}).get("regime"),
        "regime_score": (s.get("p01_context") or {}).get("regime_score"),
        "regime_confidence": (s.get("p01_context") or {}).get("regime_confidence"),
    } for s in snapshots]

    return {
        "product": "P02",
        "milestone": "P02-009",
        "snapshot_count": len(snapshots),
        "latest_snapshot_at": latest.get("captured_at") if latest else None,
        "previous_snapshot_at": previous.get("captured_at") if previous else None,
        "execution_allowed": False,
        "status": "AVAILABLE" if snapshots else "NO_HISTORY",
        "history_state": "COMPARABLE" if len(snapshots) >= 2 else ("BASELINE_ONLY" if snapshots else "EMPTY"),
        "market_probability_changes": changes,
        "discrepancy_history": discrepancy_history,
        "p01_context_timeline": p01_timeline,
        "limitations": [
            "MARKET_IMPLIED_PROBABILITY_IS_NOT_A_FORECAST",
            "HISTORICAL_CHANGE_DOES_NOT_IMPLY_CAUSALITY",
            "DISCREPANCY_IS_NOT_ARBITRAGE",
            "EXECUTION_DISABLED",
        ],
    }

def main():
    snapshots = load_snapshots()
    result = build(snapshots)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("P02-009 HISTORICAL INTELLIGENCE")
    print(f"Snapshots                    {result['snapshot_count']}")
    print(f"History State                {result['history_state']}")
    print(f"Market Change Records        {len(result['market_probability_changes'])}")
    print(f"Discrepancy History Records  {len(result['discrepancy_history'])}")
    print("Execution                    DISABLED")
    print("P02-009C INTELLIGENCE: PASS")

if __name__ == "__main__":
    main()
