#!/usr/bin/env python3
"""P02-010.6 Venue-native topic discovery.

Uses venue-native discovery surfaces instead of hoping a broad /markets page
contains every product category. Read-only; no trading/execution.
"""
from __future__ import annotations
from typing import Any
import requests

POLY_BASE="https://gamma-api.polymarket.com"
KALSHI_BASE="https://api.elections.kalshi.com/trade-api/v2"
HEADERS={"User-Agent":"P02-Prediction-Intelligence/1.0","Accept":"application/json"}

TOPICS={
 "macro":["Fed","inflation","CPI","interest rates","recession"],
 "crypto":["Bitcoin","Ethereum","crypto"],
 "metals":["gold","silver"],
 "equities":["S&P 500","Nasdaq","Nvidia","stocks"],
 "technology":["AI","OpenAI","technology"],
 "energy":["oil","energy"],
}

KALSHI_CATEGORY_HINTS={
 "macro":["Economics","Financials"],
 "crypto":["Crypto"],
 "equities":["Financials"],
 "technology":["Technology"],
 "energy":["Energy"],
}

def _get(url:str, params:dict[str,Any]|None=None, timeout:int=20)->Any:
    r=requests.get(url,params=params or {},headers=HEADERS,timeout=timeout)
    r.raise_for_status()
    return r.json()

def polymarket_topic_events(per_query:int=10, timeout:int=20)->list[dict[str,Any]]:
    """Discover events through Polymarket's native public search endpoint."""
    found=[]; seen=set()
    for topic,queries in TOPICS.items():
        for q in queries:
            try:
                payload=_get(f"{POLY_BASE}/public-search",
                             {"q":q,"limit_per_type":per_query,"keep_closed_markets":0},timeout)
            except Exception:
                continue
            events=(payload.get("events",[]) if isinstance(payload,dict) else [])
            for ev in events:
                if not isinstance(ev,dict): continue
                ident=str(ev.get("id") or ev.get("slug") or ev.get("title") or "")
                if not ident or ident in seen: continue
                seen.add(ident)
                row=dict(ev); row["_p02_discovery_topic"]=topic; row["_p02_discovery_query"]=q
                found.append(row)
    return found

def polymarket_event_markets(events:list[dict[str,Any]])->list[dict[str,Any]]:
    """Flatten nested Gamma event markets while preserving discovery metadata."""
    rows=[]; seen=set()
    for ev in events:
        for m in (ev.get("markets") or []):
            if not isinstance(m,dict): continue
            ident=str(m.get("id") or m.get("conditionId") or m.get("slug") or "")
            if not ident or ident in seen: continue
            seen.add(ident)
            x=dict(m)
            x["_p02_discovery_topic"]=ev.get("_p02_discovery_topic")
            x["_p02_discovery_query"]=ev.get("_p02_discovery_query")
            rows.append(x)
    return rows

def kalshi_series(timeout:int=20)->list[dict[str,Any]]:
    payload=_get(f"{KALSHI_BASE}/series",
                 {"include_volume":"true","include_product_metadata":"true"},timeout)
    return [x for x in payload.get("series",[]) if isinstance(x,dict)] if isinstance(payload,dict) else []

def select_kalshi_series(series:list[dict[str,Any]], per_topic:int=8)->list[dict[str,Any]]:
    """Select series using venue-provided category plus title/tags relevance."""
    selected=[]; seen=set()
    for topic,queries in TOPICS.items():
        hints={x.lower() for x in KALSHI_CATEGORY_HINTS.get(topic,[])}
        scored=[]
        for s in series:
            hay=" ".join([
                str(s.get("title") or ""), str(s.get("category") or ""),
                " ".join(str(x) for x in (s.get("tags") or []))
            ]).lower()
            category=str(s.get("category") or "").lower()
            hits=sum(1 for q in queries if q.lower() in hay)
            if category in hints: hits+=2
            if hits:
                scored.append((hits,float(s.get("volume") or 0),s))
        scored.sort(key=lambda x:(x[0],x[1]),reverse=True)
        for _,__,s in scored[:per_topic]:
            ticker=str(s.get("ticker") or "")
            key=(topic,ticker)
            if not ticker or key in seen: continue
            seen.add(key)
            x=dict(s); x["_p02_discovery_topic"]=topic
            selected.append(x)
    return selected

def kalshi_markets_for_series(series:list[dict[str,Any]], per_series:int=100, timeout:int=20)->list[dict[str,Any]]:
    rows=[]; seen=set()
    for s in series:
        ticker=s.get("ticker")
        if not ticker: continue
        try:
            payload=_get(f"{KALSHI_BASE}/markets",
                         {"status":"open","series_ticker":ticker,"limit":min(per_series,1000)},timeout)
        except Exception:
            continue
        for m in (payload.get("markets",[]) if isinstance(payload,dict) else []):
            if not isinstance(m,dict): continue
            ident=str(m.get("ticker") or "")
            if not ident or ident in seen: continue
            seen.add(ident)
            x=dict(m); x["_p02_discovery_topic"]=s.get("_p02_discovery_topic")
            rows.append(x)
    return rows
