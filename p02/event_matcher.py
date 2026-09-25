#!/usr/bin/env python3
"""P02-004 — Canonical Event Matching.

Deterministic, conservative matcher for normalized Polymarket and Kalshi records.
It intentionally prefers false negatives over false positives.
"""

from __future__ import annotations
import re
from difflib import SequenceMatcher
from typing import Any

STOPWORDS = {
    "a","an","the","is","are","will","would","be","to","of","in","on","at","by",
    "for","and","or","with","from","this","that","before","after","during","does",
    "do","did","yes","no"
}

def tokenize(text: str) -> set[str]:
    words = re.findall(r"[a-z0-9]+", (text or "").lower())
    return {w for w in words if len(w) > 1 and w not in STOPWORDS}

def lexical_similarity(a: str, b: str) -> float:
    ta, tb = tokenize(a), tokenize(b)
    if not ta or not tb:
        return 0.0
    jaccard = len(ta & tb) / len(ta | tb)
    sequence = SequenceMatcher(None, " ".join(sorted(ta)), " ".join(sorted(tb))).ratio()
    return round(0.65 * jaccard + 0.35 * sequence, 4)

def date_alignment(a: dict[str, Any], b: dict[str, Any]) -> float:
    da = (a.get("market_close_time") or "")[:10]
    db = (b.get("market_close_time") or "")[:10]
    if not da or not db:
        return 0.5
    return 1.0 if da == db else 0.0

def comparability_score(a: dict[str, Any], b: dict[str, Any]) -> float:
    lexical = lexical_similarity(a.get("question",""), b.get("question",""))
    dates = date_alignment(a, b)
    return round(0.85 * lexical + 0.15 * dates, 4)

def comparability_label(score: float) -> str:
    if score >= 0.85:
        return "HIGH"
    if score >= 0.65:
        return "MEDIUM"
    if score >= 0.40:
        return "LOW"
    return "NOT_COMPARABLE"

def match_markets(polymarket: list[dict], kalshi: list[dict]) -> list[dict]:
    candidates = []
    for p in polymarket:
        best = None
        for k in kalshi:
            score = comparability_score(p, k)
            if best is None or score > best["comparability_score"]:
                best = {
                    "polymarket": p,
                    "kalshi": k,
                    "comparability_score": score,
                    "comparability": comparability_label(score),
                }
        if best and best["comparability"] != "NOT_COMPARABLE":
            candidates.append(best)

    # One Kalshi market may only be assigned once; highest confidence wins.
    candidates.sort(key=lambda x: x["comparability_score"], reverse=True)
    used_kalshi = set()
    matches = []
    for c in candidates:
        kid = c["kalshi"]["venue_market_id"]
        if kid in used_kalshi:
            continue
        used_kalshi.add(kid)
        pid = c["polymarket"]["venue_market_id"]
        canonical = f"CANONICAL:{pid}:{kid}"
        matches.append({
            "canonical_event_id": canonical,
            "name_en": c["polymarket"]["question"],
            "name_zh_tw": "待 P02-008 UI intelligence layer 產生",
            "category": "OTHER",
            "event_window_start": None,
            "event_window_end": c["polymarket"].get("market_close_time"),
            "market_refs": [
                {"venue":"polymarket","venue_market_id":pid},
                {"venue":"kalshi","venue_market_id":kid},
            ],
            "comparability": c["comparability"],
            "comparability_score": c["comparability_score"],
            "reasons": [
                "DETERMINISTIC_LEXICAL_SIMILARITY",
                "DATE_ALIGNMENT_CHECK",
                "MANUAL_REVIEW_REQUIRED_BEFORE_EXECUTION"
            ],
        })
    return matches
