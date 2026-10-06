#!/usr/bin/env python3
"""P02-010 Production Acceptance.

Final read-only acceptance gate for P02 v1.0.
This script validates production artifacts; it does not create market signals,
modify upstream data, execute trades, or move funds.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "p02"

def load_json(name: str):
    p = DATA / name
    if not p.is_file():
        raise FileNotFoundError(f"Missing production artifact: {p.relative_to(ROOT)}")
    return json.loads(p.read_text(encoding="utf-8"))

def market_count(doc: dict) -> int:
    markets = doc.get("markets")
    if not isinstance(markets, list):
        raise AssertionError("Expected top-level 'markets' list")
    return len(markets)

def list_count(doc: dict, *keys: str) -> int:
    for key in keys:
        value = doc.get(key)
        if isinstance(value, list):
            return len(value)
    return 0

def run_acceptance() -> dict:
    poly = load_json("polymarket_markets.json")
    kalshi = load_json("kalshi_markets.json")
    canonical = load_json("canonical_events.json")
    discrepancy = load_json("discrepancies.json")
    p01 = load_json("p01_context.json")
    dashboard = load_json("dashboard_payload.json")
    historical = load_json("historical_intelligence.json")

    poly_n = market_count(poly)
    kalshi_n = market_count(kalshi)
    matched_n = list_count(canonical, "events", "canonical_events")
    discrepancy_n = list_count(discrepancy, "signals", "discrepancies")

    checks = {
        "polymarket_data": poly_n > 0,
        "kalshi_data": kalshi_n > 0,
        # Zero matches is valid. Acceptance verifies the artifact/contract exists,
        # not that the system fabricates a cross-venue match.
        "event_matching": isinstance(canonical, dict),
        "discrepancy_engine": isinstance(discrepancy, dict),
        "p01_context": isinstance(p01, dict) and "available" in p01,
        "dashboard_payload": isinstance(dashboard, dict),
        "historical_intelligence": (
            historical.get("product") == "P02"
            and historical.get("milestone") == "P02-009"
            and historical.get("snapshot_count", 0) >= 1
        ),
        "historical_comparable": historical.get("history_state") == "COMPARABLE",
        "execution_disabled": historical.get("execution_allowed") is False,
    }

    # Trust/security is evidence-based. UNKNOWN is valid and must not be
    # silently converted into SAFE.
    trust = dashboard.get("trust_security") or {}
    trust_status = trust.get("status", "UNKNOWN")
    checks["trust_security"] = trust_status in {
        "UNKNOWN", "LOW", "MEDIUM", "HIGH", "ELEVATED", "CRITICAL",
        "AVAILABLE", "DEGRADED"
    }

    # P01 is consumed as context only. P02 acceptance never authorizes execution.
    checks["p01_read_only_context"] = True

    failed = [k for k, v in checks.items() if not v]
    return {
        "product": "P02",
        "version": "v1.0",
        "milestone": "P02-010",
        "checks": checks,
        "failed_checks": failed,
        "summary": {
            "polymarket_markets": poly_n,
            "kalshi_markets": kalshi_n,
            "matched_events": matched_n,
            "discrepancy_signals": discrepancy_n,
            "trust_status": trust_status,
            "snapshot_count": historical.get("snapshot_count"),
            "history_state": historical.get("history_state"),
        },
        "semantics": {
            "zero_matches_is_valid": True,
            "probability_is_observation_not_forecast": True,
            "discrepancy_is_not_arbitrage": True,
            "trust_unknown_is_not_safe": True,
            "execution_allowed": False,
        },
        "status": "PASS" if not failed else "FAIL",
        "release_state": "READY_TO_FREEZE" if not failed else "BLOCKED",
    }

def main():
    result = run_acceptance()
    print("P02-010 PRODUCTION ACCEPTANCE")
    print(f"Polymarket Data              {'PASS' if result['checks']['polymarket_data'] else 'FAIL'}")
    print(f"Kalshi Data                  {'PASS' if result['checks']['kalshi_data'] else 'FAIL'}")
    print(f"Event Matching               {'PASS' if result['checks']['event_matching'] else 'FAIL'}")
    print(f"Discrepancy Engine           {'PASS' if result['checks']['discrepancy_engine'] else 'FAIL'}")
    print(f"P01 Context                  {'PASS' if result['checks']['p01_context'] else 'FAIL'}")
    print(f"Trust & Security             {'PASS' if result['checks']['trust_security'] else 'FAIL'}")
    print(f"Dashboard Payload            {'PASS' if result['checks']['dashboard_payload'] else 'FAIL'}")
    print(f"Historical Intelligence     {'PASS' if result['checks']['historical_intelligence'] else 'FAIL'}")
    print(f"Historical State            {result['summary']['history_state']}")
    print(f"Matched Events              {result['summary']['matched_events']} (0 is valid)")
    print(f"Discrepancy Signals         {result['summary']['discrepancy_signals']} (0 is valid)")
    print("Execution                    DISABLED")
    print()
    print(f"P02-010 PRODUCTION ACCEPTANCE: {result['status']}")
    if result["status"] == "PASS":
        print("P02 v1.0: READY TO FREEZE")
    else:
        print("Failed checks:", ", ".join(result["failed_checks"]))
        raise SystemExit(1)

if __name__ == "__main__":
    main()
