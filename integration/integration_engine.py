from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "integration" / "intelligence_overview.json"

def load_json(path):
    with open(ROOT / path, encoding="utf-8") as f:
        return json.load(f)

def build_overview():
    regime = load_json("regime_report.json")
    risk = load_json("market_risk_report.json")
    confidence = load_json("confidence_evidence_report.json")
    p02 = load_json("data/p02/dashboard_payload.json")
    predictions = p02.get("topic_intelligence", {}).get("predictions", [])

    p01 = {
        "regime": regime.get("regime", "UNKNOWN"),
        "regime_score": regime.get("score"),
        "regime_confidence": regime.get("confidence"),
        "risk_level": risk.get("risk_level", "UNKNOWN"),
        "risk_score": risk.get("risk_score"),
        "risk_confidence": risk.get("confidence"),
        "evidence_confidence": confidence.get("confidence_level", "UNKNOWN"),
        "evidence_confidence_score": confidence.get("confidence_score"),
        "evidence_coverage": confidence.get("evidence_coverage"),
        "limitations": confidence.get("limitations", []),
        "drivers": [
            {"metric_id": x.get("metric_id"), "signal_id": x.get("signal_id"),
             "direction": x.get("direction"), "strength": x.get("strength")}
            for x in regime.get("drivers", [])[:3]
        ],
    }

    linked=[]
    for x in predictions:
        cat=(x.get("category") or {}).get("key","other")
        # INT-001 foundation links context without claiming causality or directional agreement.
        direct = cat in {"macro","crypto","energy","equities","metals","technology"}
        linked.append({
            "rank": x.get("rank"),
            "event_id": x.get("event_id"),
            "question": x.get("question"),
            "venue": x.get("venue"),
            "category": x.get("category"),
            "implied_probability": x.get("implied_probability"),
            "trending_score": x.get("trending_score"),
            "context_link": "P01_CONTEXT_AVAILABLE" if direct else "NO_DIRECT_P01_CONTEXT",
            "relationship": "INSUFFICIENT_EVIDENCE",
            "relationship_reason": (
                "P01 context is relevant supporting evidence, but INT-001 does not infer causal or directional alignment without an explicit comparable rule."
                if direct else
                "No direct P01 market-context mapping is defined for this category."
            )
        })

    return {
        "product": "Intelligence Platform",
        "version": "INT-001",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "execution_allowed": False,
        "architecture": {
            "p01": "UNDERSTAND",
            "p02": "PREDICT_COMPARE",
            "integration": "CONTEXTUALIZE",
            "p03": "GOVERN_ACT_PLANNED"
        },
        "p01": p01,
        "p02": {
            "market_coverage": p02.get("summary",{}).get("polymarket_markets",0)+p02.get("summary",{}).get("kalshi_markets",0),
            "ranked_predictions": len(predictions),
            "matched_events": p02.get("summary",{}).get("matched_events",0),
            "discrepancy_signals": p02.get("summary",{}).get("discrepancy_signals",0),
            "trust_status": p02.get("summary",{}).get("trust_status","UNKNOWN"),
        },
        "integrated_intelligence": linked,
        "semantics": {
            "market_probability": "Venue-implied observation, not an INT-001 forecast.",
            "p01_context": "Supporting market context, not causal proof.",
            "relationship": "INSUFFICIENT_EVIDENCE is intentional until an explicit comparable alignment rule exists.",
            "recommendation": "No BUY/SELL/LONG/SHORT/PAY/EXECUTE recommendation is produced."
        }
    }

def main():
    data=build_overview()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print("INT-001 P01 x P02 INTEGRATION FOUNDATION: PASS")
    print("P01 regime:", data["p01"]["regime"])
    print("P01 risk:", data["p01"]["risk_level"])
    print("P02 ranked predictions:", data["p02"]["ranked_predictions"])
    print("Execution: DISABLED")

if __name__=="__main__":
    main()
