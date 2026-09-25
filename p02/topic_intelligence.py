#!/usr/bin/env python3
"""P02-010.1 topic classification and dynamic Top-20 prediction intelligence.

Deterministic/read-only. Ranks market observations; it does not forecast outcomes.
"""
from __future__ import annotations
import math, re
from collections import Counter
from typing import Any

CATEGORIES = [
    ("technology", "科技", "Technology", ["nvidia","nvda","openai","ai ","artificial intelligence","apple","iphone","tesla","spacex","microsoft","google","alphabet","meta","amazon","chip","semiconductor","robot","technology"]),
    ("equities", "股市", "Equities", ["s&p","sp 500","spy","nasdaq","dow","stock","shares","ipo","earnings","market cap","nvidia","nvda","tesla","apple","meta","coinbase"]),
    ("crypto", "加密貨幣", "Crypto", ["bitcoin","btc","ethereum","eth","crypto","solana","sol","xrp","doge","token","stablecoin","usdc","usdt","defi","blockchain"]),
    ("energy", "能源", "Energy", ["oil","wti","brent","natural gas","gas price","opec","energy","crude","uranium"]),
    ("metals", "貴金屬", "Precious Metals", ["gold","silver","platinum","palladium","precious metal"]),
    ("society", "生活議題", "Life & Society", ["weather","temperature","rain","snow","hurricane","movie","film","oscar","grammy","music","celebrity","population","climate","travel","health","social"]),
    ("politics", "政治", "Politics", ["president","presidential","election","elect","nomination","democrat","republican","congress","senate","governor","prime minister","government","policy","tariff","xi jinping","china president","fed","federal reserve","rate cut","rate hike","cpi","inflation"]),
    ("sports", "體育", "Sports", ["nba","nfl","mlb","nhl","soccer","football","basketball","baseball","tennis","ufc","f1","formula 1","championship","super bowl","world cup","goals scored","team to score"]),
]

def category_for(question: str) -> dict[str,str]:
    q=f" {question.lower()} "
    # More specific asset/topic categories win before broad politics/society.
    for key, zh, en, words in CATEGORIES:
        if any(w in q for w in words):
            return {"key":key,"zh":zh,"en":en}
    return {"key":"other","zh":"其他","en":"Other"}

def _num(x: Any) -> float:
    try: return max(0.0,float(x or 0))
    except (TypeError,ValueError): return 0.0

def _is_low_information(question: str) -> bool:
    q=question.strip().lower()
    # Kalshi combination/parlay titles can be long comma-separated outcome lists.
    return (q.startswith("yes ") and q.count(",yes ") >= 3) or len(q) > 300

def score_market(m: dict[str,Any]) -> float:
    volume=_num(m.get("volume_usd")); liquidity=_num(m.get("liquidity_usd"))
    p=_num(m.get("implied_probability"))
    score=35*min(1, math.log1p(volume)/math.log1p(1_000_000))
    score+=25*min(1, math.log1p(liquidity)/math.log1p(1_000_000))
    score+=15 if m.get("freshness")=="FRESH" else 5
    score+=10 if m.get("data_quality")=="PASS" else 0
    score+=10 if 0 < p < 1 else 0
    score+=5 if category_for(str(m.get("question","")))["key"]!="other" else 0
    if _is_low_information(str(m.get("question",""))): score-=40
    return round(max(0,score),2)

def build_top_predictions(poly: dict, kalshi: dict, limit: int=20, per_category_cap: int=5) -> dict:
    rows=[]
    for doc in (poly,kalshi):
        for m in doc.get("markets",[]):
            q=str(m.get("question") or "").strip()
            if not q: continue
            cat=category_for(q)
            rows.append({
                "event_id":m.get("event_id"), "venue":m.get("venue"), "question":q,
                "outcome":m.get("outcome"), "implied_probability":m.get("implied_probability"),
                "volume_usd":m.get("volume_usd"), "liquidity_usd":m.get("liquidity_usd"),
                "market_close_time":m.get("market_close_time"), "source_url":m.get("source_url"),
                "retrieved_at":m.get("retrieved_at"), "freshness":m.get("freshness"),
                "data_quality":m.get("data_quality"), "category":cat, "trending_score":score_market(m),
            })
    rows.sort(key=lambda x:(x["trending_score"],_num(x["volume_usd"]),_num(x["liquidity_usd"])), reverse=True)
    selected=[]; counts=Counter()
    for row in rows:
        key=row["category"]["key"]
        if counts[key]>=per_category_cap: continue
        selected.append(row); counts[key]+=1
        if len(selected)>=limit: break
    # Fill remaining slots if diversity cap prevented 20 results.
    ids={r["event_id"] for r in selected}
    for row in rows:
        if len(selected)>=limit: break
        if row["event_id"] not in ids:
            selected.append(row); ids.add(row["event_id"])
    for i,row in enumerate(selected,1): row["rank"]=i
    return {"ranking_method":"DETERMINISTIC_RELEVANCE_V1","top_n":len(selected),"category_cap":per_category_cap,
            "category_counts":dict(Counter(r["category"]["key"] for r in selected)),"predictions":selected}
