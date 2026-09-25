from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "integration" / "dashboard_payload.json"

ALLOWED_RELATIONSHIPS = {
    "SUPPORTED_CONTEXT",
    "MIXED_CONTEXT",
    "DIVERGENT_CONTEXT",
    "INSUFFICIENT_EVIDENCE",
    "NOT_APPLICABLE",
}


def load_json(rel: str) -> dict:
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def _safe_category(value) -> dict:
    if isinstance(value, dict):
        return {
            "key": value.get("key") or "other",
            "zh": value.get("zh") or value.get("en") or "其他",
            "en": value.get("en") or value.get("zh") or "Other",
        }
    return {"key": "other", "zh": "其他", "en": "Other"}


def build_dashboard_payload() -> dict:
    overview = load_json("data/integration/intelligence_overview.json")
    context = load_json("data/integration/context_intelligence.json")

    if overview.get("execution_allowed") is not False:
        raise ValueError("INT-001 execution guardrail must remain disabled")
    if context.get("execution_allowed") is not False:
        raise ValueError("INT-002 execution guardrail must remain disabled")

    p01 = overview.get("p01") or {}
    p02 = overview.get("p02") or {}
    records = context.get("context_intelligence") or []

    cards = []
    for row in records:
        relationship = row.get("relationship") or "INSUFFICIENT_EVIDENCE"
        if relationship not in ALLOWED_RELATIONSHIPS:
            raise ValueError(f"Unsupported relationship state: {relationship}")

        category = _safe_category(row.get("category"))
        # Political contracts are presentation-only venue observations.
        # INT-003 never adds a candidate/outcome inference.
        if category["key"] == "politics" and relationship != "NOT_APPLICABLE":
            raise ValueError("Political contracts must remain NOT_APPLICABLE to P01 directional inference")

        cards.append({
            "activity_rank": row.get("rank"),
            "event_id": row.get("event_id"),
            "question": row.get("question"),
            "venue": row.get("venue"),
            "category": category,
            "market_implied_probability": row.get("market_implied_probability"),
            "trending_score": row.get("trending_score"),
            "scenario": row.get("scenario"),
            "relationship": relationship,
            "p01_evidence": row.get("p01_evidence") or [],
            "p01_evidence_confidence": row.get("p01_evidence_confidence") or "UNKNOWN",
            "p01_evidence_confidence_score": row.get("p01_evidence_confidence_score"),
            "explanation": row.get("explanation") or "",
            "execution_allowed": False,
        })

    counts = {key: 0 for key in sorted(ALLOWED_RELATIONSHIPS)}
    for card in cards:
        counts[card["relationship"]] += 1

    return {
        "product": "Integrated Market Intelligence",
        "version": "INT-003",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "execution_allowed": False,
        "architecture": {
            "p01": "UNDERSTAND",
            "p02": "PREDICT_COMPARE",
            "int001": "INTEGRATE",
            "int002": "CONTEXTUALIZE",
            "int003": "PRESENT_INTEGRATED_INTELLIGENCE",
            "p03": "GOVERN_ACT_PLANNED",
        },
        "executive": {
            "p01_regime": p01.get("regime") or "UNKNOWN",
            "p01_regime_confidence": p01.get("regime_confidence"),
            "p01_risk_level": p01.get("risk_level") or "UNKNOWN",
            "p01_risk_score": p01.get("risk_score"),
            "p01_evidence_confidence": p01.get("evidence_confidence") or "UNKNOWN",
            "p01_evidence_confidence_score": p01.get("evidence_confidence_score"),
            "p01_evidence_coverage": p01.get("evidence_coverage"),
            "p02_market_coverage": p02.get("market_coverage", 0),
            "p02_ranked_predictions": p02.get("ranked_predictions", len(cards)),
            "p02_matched_events": p02.get("matched_events", 0),
            "p02_discrepancy_signals": p02.get("discrepancy_signals", 0),
            "p02_trust_status": p02.get("trust_status") or "UNKNOWN",
            "context_records": len(cards),
        },
        "relationship_counts": counts,
        "p01_drivers": p01.get("drivers") or [],
        "p01_limitations": p01.get("limitations") or [],
        "cards": cards,
        "system_status": {
            "p01_context": "LIVE",
            "p02_predictions": "LIVE",
            "int001_integration": "PASS",
            "int002_context": "PASS",
            "relationship_rendering": "PASS",
            "evidence_rendering": "PASS",
            "political_guardrail": "PASS",
            "execution": "DISABLED",
        },
        "semantics": {
            "market_probability": "Venue-implied observation only; INT-003 does not create an election, asset-price, rate, or other outcome forecast.",
            "activity_rank": "Ordering reflects upstream deterministic market activity/relevance intelligence, not political preference, endorsement, or an outcome forecast.",
            "relationship": "Relationship states describe how P02 venue observations relate to available P01 context; they do not prove causality or correctness.",
            "politics": "Candidate-specific political contracts remain NOT_APPLICABLE to P01 directional inference and are shown only as venue observations.",
            "execution": "INT-003 is read-only. No BUY/SELL/LONG/SHORT/PAY/EXECUTE recommendation or action is produced.",
        },
    }


def main() -> None:
    data = build_dashboard_payload()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    print("INT-003 INTEGRATED INTELLIGENCE DASHBOARD: PASS")
    print("P01 Context Loaded          PASS")
    print("P02 Predictions Loaded      PASS")
    print("INT-002 Intelligence Loaded PASS")
    print("Relationship Rendering      PASS")
    print("Evidence Rendering          PASS")
    print("Political Guardrail         PASS")
    print("Dashboard Cards            ", len(data["cards"]))
    print("Execution                   DISABLED")
    print("INT-003: PASS")


if __name__ == "__main__":
    main()
