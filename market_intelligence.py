"""P01-NEWS-001 Multi-Source Market & Social Intelligence Feed.

Uses the public GDELT DOC 2.0 API (no API key) for current article metadata.
Official-company queries are explicitly tagged as company-origin evidence, not independent verification.
The module never makes investment recommendations and degrades safely when sources are unavailable.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import time
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import requests

GDELT_ENDPOINT = "https://api.gdeltproject.org/api/v2/doc/doc"
SCHEMA_VERSION = "1.0"
ENGINE = "P01-NEWS-001"

TOPICS = {
    "US_MACRO": ["federal reserve", "fed", "treasury", "inflation", "cpi", "pce", "interest rate", "yield", "dollar", "dxy"],
    "WEB3_RWA": ["blockchain", "web3", "tokenization", "tokenized", "rwa", "real world asset", "onchain", "on-chain"],
    "STABLECOIN": ["stablecoin", "usdt", "usdc", "tether", "circle"],
    "DEFI": ["defi", "decentralized finance", "dex", "liquidity", "lending"],
    "AGENTIC_AI": ["ai agent", "agentic", "x402", "agent wallet", "machine payment"],
    "EXCHANGE": ["binance", "okx", "coinbase", "bybit", "bitget", "gate", "mexc", "exchange"],
    "TW_MARKET": ["taiwan", "taiwanese", "tsmc", "台灣", "台積電"],
}

OFFICIAL_DOMAINS = {
    "Binance": ["binance.com"], "OKX": ["okx.com"], "Coinbase": ["coinbase.com"],
    "Circle": ["circle.com"], "Bybit": ["bybit.com"], "Bitget": ["bitget.com"],
    "Gate": ["gate.com", "gate.io"], "MEXC": ["mexc.com", "mexc.co"],
}

GENERAL_QUERIES = {
    "US_MACRO": '("Federal Reserve" OR Treasury OR inflation OR CPI OR PCE) (markets OR crypto OR blockchain)',
    "WEB3_RWA": '(blockchain OR web3 OR tokenization OR "real world assets" OR RWA OR stablecoin OR DeFi)',
    "TW_MARKET": '(Taiwan OR TSMC) (market OR semiconductor OR blockchain OR crypto)',
}

@dataclass
class FetchResult:
    articles: list[dict[str, Any]]
    errors: list[dict[str, str]]


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def parse_seen(value: str | None) -> datetime | None:
    if not value: return None
    for fmt in ("%Y%m%dT%H%M%SZ", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%d %H:%M:%S"):
        try: return datetime.strptime(value, fmt).replace(tzinfo=timezone.utc)
        except ValueError: pass
    try: return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)
    except ValueError: return None


def gdelt_query(query: str, *, timespan: str = "2d", maxrecords: int = 75, session=requests) -> list[dict[str, Any]]:
    params={"query":query,"mode":"artlist","format":"json","maxrecords":maxrecords,"sort":"datedesc","timespan":timespan}
    last=None
    for attempt in range(2):
        try:
            r=session.get(GDELT_ENDPOINT, params=params, timeout=8, headers={"User-Agent":"MacroWeb3RiskIntelligence/1.0"})
            r.raise_for_status()
            payload=r.json()
            return payload.get("articles", []) if isinstance(payload, dict) else []
        except Exception as exc:
            last=exc
            if attempt < 1: time.sleep(1.0)
    raise RuntimeError(f"GDELT query failed: {last}")


def canonical_domain(url: str, fallback: str = "") -> str:
    try: return urlparse(url).netloc.lower().removeprefix("www.") or fallback.lower()
    except Exception: return fallback.lower()


def classify(text: str) -> list[str]:
    s=text.lower()
    scored=[]
    for topic, words in TOPICS.items():
        score=sum(1 for w in words if w in s)
        if score: scored.append((score, topic))
    return [t for _,t in sorted(scored, reverse=True)] or ["WEB3_RWA"]


def freshness(dt: datetime | None, now: datetime) -> str:
    if not dt: return "UNKNOWN"
    age=now-dt
    if age <= timedelta(hours=36): return "FRESH"
    if age <= timedelta(days=7): return "STALE"
    return "ARCHIVED"


def item_id(url: str, title: str) -> str:
    return "NEWS-"+hashlib.sha256((url.strip()+"|"+title.strip()).encode()).hexdigest()[:12].upper()


def normalize_article(raw: dict[str, Any], *, evidence_type: str, company: str | None, now: datetime) -> dict[str, Any] | None:
    url=str(raw.get("url") or "").strip(); title=str(raw.get("title") or "").strip()
    if not url or not title: return None
    published=parse_seen(raw.get("seendate")); domain=canonical_domain(url, str(raw.get("domain") or ""))
    topics=classify(" ".join([title, company or "", domain]))
    status=freshness(published, now)
    return {
        "id": item_id(url,title), "title": title, "url": url, "domain": domain,
        "source_name": company or domain or "Unknown source", "source_type": evidence_type,
        "published_at": published.isoformat().replace("+00:00","Z") if published else None,
        "freshness": status, "language": raw.get("language"), "source_country": raw.get("sourcecountry"),
        "topics": topics, "primary_topic": topics[0],
        "why_it_matters": build_context(topics),
        "linked_p01_context": linked_context(topics),
        "evidence_note": "Company-origin announcement; treat as first-party evidence." if evidence_type=="OFFICIAL_COMPANY_SOURCE" else "External news metadata; verify material claims at the original source.",
        "limitations": "Association with P01 context does not establish causality or constitute an investment recommendation."
    }


def build_context(topics: list[str]) -> str:
    mapping={
        "US_MACRO":"Macro policy and rates can affect liquidity, USD conditions, and cross-asset risk context.",
        "STABLECOIN":"Stablecoin developments can affect payment rails, on-chain liquidity, and institutional adoption.",
        "WEB3_RWA":"Web3/RWA developments can affect tokenization infrastructure and institutional on-chain adoption.",
        "DEFI":"DeFi developments can affect on-chain liquidity, credit, and protocol risk context.",
        "AGENTIC_AI":"Agentic finance developments are relevant to autonomous authorization and payment infrastructure.",
        "EXCHANGE":"Exchange developments can affect market access, liquidity, compliance, and infrastructure.",
        "TW_MARKET":"Taiwan market developments can affect semiconductor and cross-market risk context.",
    }
    return mapping.get(topics[0], mapping["WEB3_RWA"])


def linked_context(topics: list[str]) -> list[str]:
    out=[]
    if "US_MACRO" in topics: out += ["US10Y", "DXY", "MARKET_REGIME", "MARKET_RISK"]
    if any(t in topics for t in ("WEB3_RWA","STABLECOIN","DEFI","AGENTIC_AI","EXCHANGE")): out += ["BTC", "ETH", "MARKET_REGIME", "EVIDENCE_CONFIDENCE"]
    if "TW_MARKET" in topics: out += ["MARKET_REGIME", "MARKET_RISK"]
    return list(dict.fromkeys(out))


def dedupe(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen=set(); out=[]
    for x in sorted(items, key=lambda a:a.get("published_at") or "", reverse=True):
        key=(x.get("url") or "").split("?")[0].rstrip("/").lower()
        if not key: key=re.sub(r"\W+"," ",x.get("title","").lower()).strip()
        if key in seen: continue
        seen.add(key); out.append(x)
    return out


def fetch_feed() -> dict[str, Any]:
    now=datetime.now(timezone.utc); items=[]; errors=[]; source_status=[]
    for label,q in GENERAL_QUERIES.items():
        try:
            raws=gdelt_query(q, timespan="2d", maxrecords=60)
            count=0
            for raw in raws:
                item=normalize_article(raw,evidence_type="NEWS_SOURCE",company=None,now=now)
                if item: items.append(item); count+=1
            source_status.append({"source":f"GDELT:{label}","status":"OK","items":count})
        except Exception as exc:
            errors.append({"source":f"GDELT:{label}","error":str(exc)}); source_status.append({"source":f"GDELT:{label}","status":"UNAVAILABLE","items":0})
    for company,domains in OFFICIAL_DOMAINS.items():
        q=" OR ".join(f"domain:{d}" for d in domains)
        try:
            raws=gdelt_query(f"({q}) (blockchain OR crypto OR web3 OR stablecoin OR token OR payment OR DeFi OR RWA OR AI)",timespan="7d",maxrecords=30)
            count=0
            for raw in raws:
                dom=canonical_domain(str(raw.get("url") or ""),str(raw.get("domain") or ""))
                if not any(dom==d or dom.endswith("."+d) for d in domains): continue
                item=normalize_article(raw,evidence_type="OFFICIAL_COMPANY_SOURCE",company=company,now=now)
                if item: items.append(item); count+=1
            source_status.append({"source":company,"status":"OK","items":count})
        except Exception as exc:
            errors.append({"source":company,"error":str(exc)}); source_status.append({"source":company,"status":"UNAVAILABLE","items":0})
    items=[x for x in dedupe(items) if x["freshness"] in {"FRESH","STALE"}]
    # Keep a bounded feed for GitHub Pages; official first when timestamps tie.
    items=sorted(items,key=lambda x:(x.get("published_at") or "", x["source_type"]=="OFFICIAL_COMPANY_SOURCE"),reverse=True)[:90]
    return {"schema_version":SCHEMA_VERSION,"engine":ENGINE,"generated_at":now_iso(),"status":"AVAILABLE" if items else "UNAVAILABLE","sources":source_status,"errors":errors,"items":items,
            "social_adapters":{"X":"NOT_CONFIGURED","Threads":"PHASE_2"},
            "methodology":{"source_hierarchy":["OFFICIAL_COMPANY_SOURCE","NEWS_SOURCE","SOCIAL_SIGNAL"],"freshness":{"FRESH":"<=36h","STALE":"<=7d","ARCHIVED":">7d"},"principles":["Source provenance is explicit.","First-party announcements are not independent verification.","News-to-market matching is contextual association, not causal proof.","No investment recommendation."]}}


def validate_feed(feed: dict[str, Any]) -> None:
    assert feed.get("schema_version")==SCHEMA_VERSION and feed.get("engine")==ENGINE
    assert feed.get("status") in {"AVAILABLE","UNAVAILABLE"}
    assert isinstance(feed.get("items"),list)
    for x in feed["items"]:
        for k in ("id","title","url","source_name","source_type","freshness","topics","linked_p01_context","limitations"): assert k in x, k
        assert x["source_type"] in {"OFFICIAL_COMPANY_SOURCE","NEWS_SOURCE","SOCIAL_SIGNAL"}
        assert x["freshness"] in {"FRESH","STALE","ARCHIVED","UNKNOWN"}
        assert x["url"].startswith(("http://","https://"))


def main() -> int:
    ap=argparse.ArgumentParser(); ap.add_argument("--output",default="market_intelligence_feed.json"); ap.add_argument("--strict",action="store_true")
    args=ap.parse_args(); feed=fetch_feed(); validate_feed(feed)
    Path(args.output).write_text(json.dumps(feed,ensure_ascii=False,indent=2),encoding="utf-8")
    print(f"{ENGINE}: {feed['status']} | {len(feed['items'])} items | {len(feed['errors'])} source errors")
    if args.strict and feed["status"]!="AVAILABLE": return 2
    return 0
if __name__=="__main__": raise SystemExit(main())
