#!/usr/bin/env python3
"""P02-007/008 data builder for the static GitHub Pages dashboard."""
from __future__ import annotations
import json, sys
from pathlib import Path
from datetime import datetime, timezone

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from p02.trust_security import aggregate_trust
from p02.topic_intelligence import build_top_predictions

def load(path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default

def main():
    data=ROOT/"data/p02"
    poly=load(data/"polymarket_markets.json",{"markets":[]})
    kalshi=load(data/"kalshi_markets.json",{"markets":[]})
    canonical=load(data/"canonical_events.json",{"events":[]})
    discrepancies=load(data/"discrepancies.json",{"signals":[]})
    context=load(data/"p01_context.json",{"available":False})

    # Security feed is intentionally optional at P02-007.
    secdoc=load(data/"security_events.json",{"events":[]})
    events=secdoc.get("events",[])
    trust=aggregate_trust(events)
    topic_intelligence=build_top_predictions(poly, kalshi, limit=20, per_category_cap=5)

    payload={
        "product":"P02",
        "version":"P02-010.1",
        "generated_at":datetime.now(timezone.utc).isoformat().replace("+00:00","Z"),
        "execution_allowed":False,
        "summary":{
            "polymarket_markets":len(poly.get("markets",[])),
            "kalshi_markets":len(kalshi.get("markets",[])),
            "matched_events":len(canonical.get("events",[])),
            "discrepancy_signals":len(discrepancies.get("signals",[])),
            "p01_context_available":bool(context.get("available")),
            "trust_status":trust["status"],
        },
        "topic_intelligence":topic_intelligence,
        "trust_security":trust,
        "security_events":events,
        "canonical_events":canonical.get("events",[]),
        "discrepancies":discrepancies.get("signals",[]),
        "p01_context":{
            "available":bool(context.get("available")),
            "mode":context.get("mode","READ_ONLY"),
            "interpretation_rule":context.get("interpretation_rule","P01 context is supporting evidence, not causal proof.")
        },
        "limitations":[
            "MARKET_IMPLIED_PROBABILITY_IS_NOT_A_FORECAST",
            "DISCREPANCY_IS_NOT_ARBITRAGE",
            "TRUST_STATUS_IS_NOT_A SAFETY_GUARANTEE",
            "EXECUTION_DISABLED"
        ]
    }

    out=data/"dashboard_payload.json"
    out.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("P02 BATCH B")
    print("P02-007 Trust & Security     PASS")
    print(f"Trust Status                 {trust['status']}")
    print(f"Security Events              {trust['event_count']}")
    print("P02-008 Dashboard Payload    PASS")
    print(f"Polymarket Markets           {payload['summary']['polymarket_markets']}")
    print(f"Kalshi Markets               {payload['summary']['kalshi_markets']}")
    print(f"Matched Events               {payload['summary']['matched_events']}")
    print(f"Discrepancy Signals          {payload['summary']['discrepancy_signals']}")
    print("Execution                    DISABLED")
    print("P02 BATCH B: PASS")
if __name__=="__main__":
    main()
