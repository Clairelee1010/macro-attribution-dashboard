#!/usr/bin/env python3
"""P02-010.4 Category-Aware Market Discovery.

Selects a diverse candidate pool from already-normalized venue records.
It does not forecast, alter probabilities, or fabricate categories.
"""
from __future__ import annotations
from collections import Counter
from typing import Any
from p02.topic_intelligence import category_for

DISCOVERY_CATEGORIES = (
    "technology","equities","crypto","macro","energy","metals",
    "society","politics","sports","other",
)

def _num(v: Any) -> float:
    try: return max(0.0, float(v or 0))
    except (TypeError, ValueError): return 0.0

def discovery_score(m: dict[str, Any]) -> float:
    # Transparent source-discovery score. Existing Trending scoring remains downstream.
    volume = _num(m.get("volume_usd"))
    liquidity = _num(m.get("liquidity_usd"))
    freshness = 1.0 if m.get("freshness") == "FRESH" else 0.0
    quality = 1.0 if m.get("data_quality") == "PASS" else 0.0
    return volume + 0.35 * liquidity + 10_000 * freshness + 10_000 * quality

def discover_balanced(markets: list[dict[str, Any]], per_category: int = 25,
                      total_limit: int = 250) -> tuple[list[dict[str, Any]], dict[str,int]]:
    buckets={k:[] for k in DISCOVERY_CATEGORIES}
    for m in markets:
        q=str(m.get("question") or "").strip()
        if not q: continue
        key=category_for(q)["key"]
        buckets.setdefault(key,[]).append(m)

    selected=[]
    for key in DISCOVERY_CATEGORIES:
        rows=sorted(
            buckets.get(key,[]),
            key=lambda m:(discovery_score(m), _num(m.get("volume_usd")), _num(m.get("liquidity_usd"))),
            reverse=True,
        )
        selected.extend(rows[:per_category])

    # Deduplicate by venue:event_id while preserving category round selection.
    dedup=[]
    seen=set()
    for m in selected:
        ident=(m.get("venue"),m.get("event_id"))
        if ident in seen: continue
        seen.add(ident); dedup.append(m)

    # If category buckets don't fill the pool, add best remaining candidates.
    if len(dedup) < total_limit:
        remaining=sorted(markets,key=discovery_score,reverse=True)
        for m in remaining:
            ident=(m.get("venue"),m.get("event_id"))
            if ident in seen: continue
            dedup.append(m); seen.add(ident)
            if len(dedup)>=total_limit: break

    dedup=dedup[:total_limit]
    counts=Counter(category_for(str(m.get("question") or ""))["key"] for m in dedup)
    return dedup, dict(counts)

def discovery_report(poly: dict, kalshi: dict, per_category: int = 25,
                     total_limit: int = 250) -> dict:
    all_markets=list(poly.get("markets",[]))+list(kalshi.get("markets",[]))
    selected, counts=discover_balanced(all_markets,per_category,total_limit)
    return {
        "method":"CATEGORY_AWARE_DISCOVERY_V1",
        "candidate_count":len(all_markets),
        "selected_count":len(selected),
        "per_category_target":per_category,
        "category_counts":counts,
        "markets":selected,
        "execution_allowed":False,
    }
