#!/usr/bin/env python3
"""P02-005 — Cross-market discrepancy engine."""

from __future__ import annotations
from typing import Any

def attention_level(gap_pp: float, comparability: str) -> str:
    if comparability == "NOT_COMPARABLE":
        return "SUPPRESSED"
    if gap_pp >= 8:
        return "HIGH_ATTENTION"
    if gap_pp >= 4:
        return "MEDIUM_ATTENTION"
    return "LOW_ATTENTION"

def evidence_confidence(match: dict[str, Any], p: dict[str, Any], k: dict[str, Any]) -> str:
    score = float(match.get("comparability_score", 0))
    fresh = p.get("freshness") == "FRESH" and k.get("freshness") == "FRESH"
    quality = p.get("data_quality") == "PASS" and k.get("data_quality") == "PASS"
    if score >= 0.85 and fresh and quality:
        return "HIGH"
    if score >= 0.65 and quality:
        return "MEDIUM"
    return "LOW"

def build_discrepancy(match: dict[str, Any], p: dict[str, Any], k: dict[str, Any]) -> dict[str, Any]:
    pp = float(p["implied_probability"])
    kp = float(k["implied_probability"])
    gap = round(abs(pp-kp)*100, 2)
    return {
        "signal_id": f"DISC:{match['canonical_event_id']}",
        "canonical_event_id": match["canonical_event_id"],
        "market_probabilities": [
            {"venue":"polymarket","probability":pp},
            {"venue":"kalshi","probability":kp},
        ],
        "raw_discrepancy_pp": gap,
        "comparability": match["comparability"],
        "evidence_confidence": evidence_confidence(match,p,k),
        "attention": attention_level(gap, match["comparability"]),
        "trust_status": "UNKNOWN",
        "execution_allowed": False,
        "reasons": [
            f"CROSS_MARKET_GAP_{gap}PP",
            f"COMPARABILITY_{match['comparability']}",
            "MARKET_IMPLIED_PROBABILITIES_ONLY"
        ],
        "limitations": [
            "DISCREPANCY_IS_NOT_ARBITRAGE",
            "PROBABILITY_IS_NOT_OBJECTIVE_TRUTH",
            "CONTRACT_TERMS_MAY_DIFFER",
            "NO_EXECUTION_AUTHORIZED"
        ]
    }
