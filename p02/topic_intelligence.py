#!/usr/bin/env python3
"""P02-010.2 topic classification quality + dynamic Top-20 intelligence.

Deterministic/read-only. Classifies and ranks market observations; it does not
forecast outcomes. Classification uses explicit regex rules to avoid substring
collisions such as ETH inside "Kenneth".
"""
from __future__ import annotations
import math, re
from collections import Counter
from typing import Any

CATEGORY_LABELS = {
    "technology": ("科技", "Technology"),
    "equities": ("股市", "Equities"),
    "crypto": ("加密貨幣", "Crypto"),
    "macro": ("總經／利率", "Macro & Rates"),
    "energy": ("能源", "Energy"),
    "metals": ("貴金屬", "Precious Metals"),
    "society": ("生活議題", "Life & Society"),
    "politics": ("政治", "Politics"),
    "sports": ("體育", "Sports"),
    "other": ("其他", "Other"),
}

# Ordered by semantic specificity. Regex boundaries prevent accidental substring
# matches (e.g. "eth" in Kenneth, "sol" in resolution).
RULES = [
    ("sports", [
        r"\bnba\b", r"\bnfl\b", r"\bmlb\b", r"\bnhl\b", r"\bwnba\b",
        r"\bsoccer\b", r"\bfootball\b", r"\bbasketball\b", r"\bbaseball\b",
        r"\btennis\b", r"\bufc\b", r"\bformula\s*1\b", r"\bf1\b",
        r"\bsuper bowl\b", r"\bworld cup\b", r"\bchampionship\b",
        r"\bplayoffs?\b", r"\btouchdowns?\b", r"\bpassing yards?\b",
        r"\brushing yards?\b", r"\breceiving yards?\b", r"\bgoals?\b",
        r"\bpoints?\b.*\b(?:player|game|match)\b",
        # Common sports parlay phrasing visible in Kalshi titles.
        r"\b(?:dalton schultz|rashee rice|romeo doubs|garrett wilson|derrick henry|kenneth walker|breece hall)\b",
    ]),
    ("politics", [
        r"\bpresident(?:ial)?\b", r"\belections?\b", r"\belected\b",
        r"\bnomination\b", r"\bdemocrat(?:ic)?\b", r"\brepublican\b",
        r"\bcongress\b", r"\bsenate\b", r"\bgovernor\b", r"\bprime minister\b",
        r"\bparliament\b", r"\bgovernment\b", r"\bwhite house\b",
        r"\bxi jinping\b", r"\bputin\b", r"\btrump\b",
        r"\bpolitic(?:s|al)?\b",
    ]),
    ("macro", [
        r"\bfederal reserve\b", r"\bfed\b", r"\bfomc\b",
        r"\brate cuts?\b", r"\brate hikes?\b", r"\binterest rates?\b",
        r"\bcpi\b", r"\binflation\b", r"\bgdp\b", r"\bunemployment\b",
        r"\bpayrolls?\b", r"\btreasury\b", r"\byield curve\b",
        r"\brecession\b",
    ]),
    ("metals", [
        r"\bgold\b", r"\bsilver\b", r"\bplatinum\b", r"\bpalladium\b",
        r"\bprecious metals?\b",
    ]),
    ("energy", [
        r"\boil\b", r"\bwti\b", r"\bbrent\b", r"\bcrude\b",
        r"\bnatural gas\b", r"\bopec\b", r"\buranium\b",
        r"\benergy prices?\b",
    ]),
    ("crypto", [
        r"\bbitcoin\b", r"\bbtc\b", r"\bethereum\b", r"\beth\b",
        r"\bcrypto(?:currency)?\b", r"\bsolana\b", r"\bsol\b",
        r"\bxrp\b", r"\bdogecoin\b", r"\bdoge\b", r"\bstablecoins?\b",
        r"\busdc\b", r"\busdt\b", r"\bdefi\b", r"\bblockchain\b",
        r"\btokenized?\b", r"\bweb3\b",
    ]),
    ("equities", [
        r"\bs&p\s*500\b", r"\bspx\b", r"\bspy\b", r"\bnasdaq\b",
        r"\bdow(?: jones)?\b", r"\bstocks?\b", r"\bshares?\b",
        r"\bipo\b", r"\bearnings\b", r"\bmarket cap\b",
        r"\bnvda\b", r"\bnvidia\b", r"\bcoinbase\b",
        r"\btesla\b", r"\bapple\b", r"\bmeta\b", r"\bmicrosoft\b",
        r"\balphabet\b", r"\bamazon\b",
    ]),
    ("technology", [
        r"\bopenai\b", r"\bartificial intelligence\b", r"\bai model\b",
        r"\biphone\b", r"\bspacex\b", r"\bsemiconductors?\b",
        r"\bchips?\b", r"\brobots?\b", r"\btechnology\b",
    ]),
    ("society", [
        r"\bweather\b", r"\btemperature\b", r"\brain\b", r"\bsnow\b",
        r"\bhurricane\b", r"\bclimate\b", r"\bmovie\b", r"\bfilm\b",
        r"\boscar\b", r"\bgrammy\b", r"\bmusic\b", r"\bcelebrity\b",
        r"\bpopulation\b", r"\btravel\b", r"\bhealth\b",
    ]),
]
COMPILED_RULES = [(key, [re.compile(p, re.I) for p in patterns]) for key, patterns in RULES]

def _category(key: str) -> dict[str, str]:
    zh, en = CATEGORY_LABELS[key]
    return {"key": key, "zh": zh, "en": en}

def category_for(question: str) -> dict[str, str]:
    q = " ".join(str(question or "").split())
    for key, patterns in COMPILED_RULES:
        if any(p.search(q) for p in patterns):
            return _category(key)
    return _category("other")

def _num(x: Any) -> float:
    try:
        return max(0.0, float(x or 0))
    except (TypeError, ValueError):
        return 0.0

def _is_low_information(question: str) -> bool:
    """Reject unreadable multi-leg/parlay-style titles from Trending intelligence.

    These may be valid venue contracts, but they are poor human-facing
    intelligence topics. P02 keeps them in raw venue data; it only excludes
    them from the curated Trending view.
    """
    q = " ".join(str(question or "").strip().lower().split())
    legs = q.count(",yes ") + q.count(",no ")
    starts_leg = q.startswith("yes ") or q.startswith("no ")
    sports_combo_terms = len(re.findall(
        r"\b(?:points? scored|goals? scored|wins? by over|wins? by more than|"
        r"rushing yards?|receiving yards?|passing yards?)\b", q
    ))
    return (
        len(q) > 240
        or (starts_leg and legs >= 2)
        or sports_combo_terms >= 3
    )

def _has_usable_market_observation(m: dict[str, Any]) -> bool:
    """Quality gate for the human-facing Trending list."""
    p = m.get("implied_probability")
    try:
        p = float(p)
    except (TypeError, ValueError):
        return False
    if not (0 < p < 1):
        return False
    # Require at least one activity/liquidity signal so zero-information
    # contracts do not enter Trending merely to fill a quota.
    return _num(m.get("volume_usd")) > 0 or _num(m.get("liquidity_usd")) > 0

def score_market(m: dict[str, Any]) -> float:
    volume = _num(m.get("volume_usd"))
    liquidity = _num(m.get("liquidity_usd"))
    p = _num(m.get("implied_probability"))
    score = 35 * min(1, math.log1p(volume) / math.log1p(1_000_000))
    score += 25 * min(1, math.log1p(liquidity) / math.log1p(1_000_000))
    score += 15 if m.get("freshness") == "FRESH" else 5
    score += 10 if m.get("data_quality") == "PASS" else 0
    score += 10 if 0 < p < 1 else 0
    score += 5 if category_for(str(m.get("question", "")))["key"] != "other" else 0
    if _is_low_information(str(m.get("question", ""))):
        score -= 40
    return round(max(0, score), 2)

def build_top_predictions(poly: dict, kalshi: dict, limit: int = 20, per_category_cap: int = 5) -> dict:
    rows = []
    for doc in (poly, kalshi):
        for m in doc.get("markets", []):
            q = str(m.get("question") or "").strip()
            if not q or _is_low_information(q) or not _has_usable_market_observation(m):
                continue
            cat = category_for(q)
            rows.append({
                "event_id": m.get("event_id"),
                "venue": m.get("venue"),
                "question": q,
                "outcome": m.get("outcome"),
                "implied_probability": m.get("implied_probability"),
                "volume_usd": m.get("volume_usd"),
                "liquidity_usd": m.get("liquidity_usd"),
                "market_close_time": m.get("market_close_time"),
                "source_url": m.get("source_url"),
                "retrieved_at": m.get("retrieved_at"),
                "freshness": m.get("freshness"),
                "data_quality": m.get("data_quality"),
                "category": cat,
                "trending_score": score_market(m),
            })

    rows.sort(
        key=lambda x: (x["trending_score"], _num(x["volume_usd"]), _num(x["liquidity_usd"])),
        reverse=True,
    )

    selected, counts = [], Counter()
    for row in rows:
        key = row["category"]["key"]
        if counts[key] >= per_category_cap:
            continue
        selected.append(row)
        counts[key] += 1
        if len(selected) >= limit:
            break

    for i, row in enumerate(selected, 1):
        row["rank"] = i

    return {
        "ranking_method": "DETERMINISTIC_RELEVANCE_V3_QUALITY_GATED",
        "top_n": len(selected),
        "requested_top_n": limit,
        "quality_policy": "UP_TO_20_NO_FORCED_FILL",
        "category_cap": per_category_cap,
        "category_counts": dict(Counter(r["category"]["key"] for r in selected)),
        "predictions": selected,
    }
