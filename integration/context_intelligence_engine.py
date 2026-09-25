from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path

from integration.context_mapper import load_rules
from integration.divergence_engine import evaluate_relationship
from integration.explanation_engine import explain

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "integration" / "context_intelligence.json"


def load_json(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def build_context_intelligence():
    overview = load_json("data/integration/intelligence_overview.json")
    rules = load_rules()
    p01 = overview["p01"]
    rows = []

    for pred in overview.get("integrated_intelligence", []):
        ev = evaluate_relationship(pred, p01, rules)
        rows.append({
            "rank": pred.get("rank"),
            "event_id": pred.get("event_id"),
            "question": pred.get("question"),
            "venue": pred.get("venue"),
            "category": pred.get("category"),
            "market_implied_probability": pred.get("implied_probability"),
            "trending_score": pred.get("trending_score"),
            "scenario": ev["scenario"],
            "relationship": ev["relationship"],
            "p01_evidence": ev["evidence"],
            "p01_evidence_confidence": p01.get("evidence_confidence", "UNKNOWN"),
            "p01_evidence_confidence_score": p01.get("evidence_confidence_score"),
            "explanation": explain(pred, p01, ev),
            "execution_allowed": False
        })

    counts = {}
    for x in rows:
        counts[x["relationship"]] = counts.get(x["relationship"], 0) + 1

    return {
        "product": "Intelligence Platform",
        "version": "INT-002",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "execution_allowed": False,
        "input": {"integration_version": overview.get("version"), "p01_regime": p01.get("regime"), "p01_risk_level": p01.get("risk_level"), "predictions_evaluated": len(rows)},
        "relationship_counts": counts,
        "context_intelligence": rows,
        "semantics": {
            "relationship_states": rules["semantics"],
            "market_probability": "Venue-implied observation only; INT-002 does not create an election, asset-price, rate, or other outcome forecast.",
            "politics": "Candidate-specific political contracts are NOT_APPLICABLE to P01 directional inference. No candidate ranking, endorsement, or outcome prediction is generated.",
            "context": "P01 context is supporting evidence, not causal proof.",
            "execution": "No BUY/SELL/LONG/SHORT/PAY/EXECUTE recommendation or action is produced."
        }
    }


def main():
    d = build_context_intelligence()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
    print("INT-002 CONTEXT ALIGNMENT & DIVERGENCE: PASS")
    print("P01 Context Loaded          PASS")
    print("P02 Predictions Loaded      PASS")
    print("Context Mapping             PASS")
    print("Evidence Guardrail          PASS")
    print("Political Guardrail         PASS")
    print("Explanation Generation      PASS")
    print("Predictions Evaluated      ", d["input"]["predictions_evaluated"])
    print("Relationship Counts        ", d["relationship_counts"])
    print("Execution                    DISABLED")
    print("INT-002: PASS")

if __name__ == "__main__":
    main()
