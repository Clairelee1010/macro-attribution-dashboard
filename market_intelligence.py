"""P01-NEWS-003 Live Source Expansion.

Primary: GDELT DOC 2.0.
Fallback: Google News RSS (keyless).

Sources are fetched concurrently with bounded timeouts so one outage
cannot stall CI.

P01-NEWS-003 expands first-party source coverage across:
- US macro / regulation
- Web3 / stablecoin / exchanges
- Taiwan market / semiconductor

No investment recommendation.
Stale prototype content is never promoted as CURRENT.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re

from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Any
from urllib.parse import quote_plus, urlparse

import xml.etree.ElementTree as ET
import requests


# ============================================================
# P01-NEWS-003
# Live Market Intelligence Source Layer
# ============================================================

GDELT_ENDPOINT = "https://api.gdeltproject.org/api/v2/doc/doc"
GOOGLE_RSS_ENDPOINT = "https://news.google.com/rss/search"

SCHEMA_VERSION = "1.0"
ENGINE = "P01-NEWS-003"

REQUEST_TIMEOUT = 5
MAX_WORKERS = 8


# ============================================================
# Topic Classification
# ============================================================

TOPICS = {
    "US_MACRO": [
        "federal reserve",
        "fed",
        "treasury",
        "inflation",
        "cpi",
        "pce",
        "interest rate",
        "yield",
        "dollar",
        "dxy",
    ],

    "WEB3_RWA": [
        "blockchain",
        "web3",
        "tokenization",
        "tokenized",
        "rwa",
        "real world asset",
        "onchain",
        "on-chain",
    ],

    "STABLECOIN": [
        "stablecoin",
        "usdt",
        "usdc",
        "tether",
        "circle",
    ],

    "DEFI": [
        "defi",
        "decentralized finance",
        "dex",
        "liquidity",
        "lending",
    ],

    "AGENTIC_AI": [
        "ai agent",
        "agentic",
        "x402",
        "agent wallet",
        "machine payment",
    ],

    "EXCHANGE": [
        "binance",
        "okx",
        "coinbase",
        "bybit",
        "bitget",
        "gate",
        "mexc",
        "exchange",
    ],

    "TW_MARKET": [
        "taiwan",
        "taiwanese",
        "tsmc",
        "台灣",
        "台積電",
    ],
}


# ============================================================
# Official / First-Party Sources
# ============================================================

OFFICIAL_DOMAINS = {
    # --------------------------------------------------------
    # US Macro / Regulation
    # --------------------------------------------------------
    "Federal Reserve": [
        "federalreserve.gov",
    ],

    "SEC": [
        "sec.gov",
    ],

    "US Treasury": [
        "treasury.gov",
    ],

    # --------------------------------------------------------
    # Web3 / Stablecoin / Exchanges
    # --------------------------------------------------------
    "Binance": [
        "binance.com",
    ],

    "OKX": [
        "okx.com",
    ],

    "Coinbase": [
        "coinbase.com",
    ],

    "Circle": [
        "circle.com",
    ],

    "Bybit": [
        "bybit.com",
    ],

    "Bitget": [
        "bitget.com",
    ],

    "Gate": [
        "gate.com",
        "gate.io",
    ],

    "MEXC": [
        "mexc.com",
        "mexc.co",
    ],

    # --------------------------------------------------------
    # Taiwan
    # --------------------------------------------------------
    "TWSE": [
        "twse.com.tw",
    ],

    "TSMC": [
        "tsmc.com",
    ],
}


# ============================================================
# General News Queries
# ============================================================

GENERAL_QUERIES = {
    "US_MACRO":
        "Federal Reserve Treasury inflation CPI PCE markets crypto blockchain",

    "WEB3_RWA":
        "blockchain web3 tokenization real world assets RWA stablecoin DeFi",

    "TW_MARKET":
        "Taiwan TSMC market semiconductor blockchain crypto",
}


# ============================================================
# Source-specific Official Queries
#
# Important:
# Do not use one generic Web3 query for every official source.
# Fed / Treasury / TWSE require domain-specific search terms.
# ============================================================

OFFICIAL_QUERIES = {
    # US Macro / Regulation
    "Federal Reserve":
        "interest rate monetary policy inflation liquidity markets",

    "SEC":
        "crypto digital asset token securities blockchain",

    "US Treasury":
        "treasury yield financial markets digital assets",

    # Web3 / Exchanges
    "Binance":
        "blockchain crypto web3 stablecoin token DeFi RWA AI",

    "OKX":
        "blockchain crypto web3 stablecoin token DeFi RWA AI",

    "Coinbase":
        "blockchain crypto web3 stablecoin token DeFi RWA AI",

    "Circle":
        "stablecoin USDC payment blockchain tokenization",

    "Bybit":
        "blockchain crypto web3 stablecoin token DeFi RWA AI",

    "Bitget":
        "blockchain crypto web3 stablecoin token DeFi RWA AI",

    "Gate":
        "blockchain crypto web3 stablecoin token DeFi RWA AI",

    "MEXC":
        "blockchain crypto web3 stablecoin token DeFi RWA AI",

    # Taiwan
    "TWSE":
        "Taiwan market semiconductor TSMC ETF",

    "TSMC":
        "semiconductor AI market technology",
}


# ============================================================
# Source Task
# ============================================================

@dataclass
class SourceTask:
    label: str
    query: str
    company: str | None = None
    domains: list[str] | None = None
    timespan: str = "2d"
    maxrecords: int = 60


# ============================================================
# Time Helpers
# ============================================================

def now_iso():
    return (
        datetime.now(timezone.utc)
        .isoformat()
        .replace("+00:00", "Z")
    )


def parse_seen(v):
    if not v:
        return None

    for f in (
        "%Y%m%dT%H%M%SZ",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%d %H:%M:%S",
    ):
        try:
            return datetime.strptime(v, f).replace(tzinfo=timezone.utc)
        except ValueError:
            pass

    try:
        return parsedate_to_datetime(v).astimezone(timezone.utc)
    except Exception:
        pass

    try:
        return datetime.fromisoformat(
            v.replace("Z", "+00:00")
        ).astimezone(timezone.utc)
    except Exception:
        return None


# ============================================================
# GDELT Provider
# ============================================================

def gdelt_query(
    query,
    timespan="2d",
    maxrecords=75,
    session=requests,
):
    params = {
        "query": query,
        "mode": "artlist",
        "format": "json",
        "maxrecords": maxrecords,
        "sort": "datedesc",
        "timespan": timespan,
    }

    r = session.get(
        GDELT_ENDPOINT,
        params=params,
        timeout=REQUEST_TIMEOUT,
        headers={
            "User-Agent":
                "MacroWeb3RiskIntelligence/1.1"
        },
    )

    r.raise_for_status()

    payload = r.json()

    return (
        payload.get("articles", [])
        if isinstance(payload, dict)
        else []
    )


# ============================================================
# Google News RSS Fallback
# ============================================================

def google_news_query(
    query,
    maxrecords=75,
    session=requests,
):
    # Public RSS fallback; no API key.
    # Link may be a Google News redirect to the publisher.

    url = (
        f"{GOOGLE_RSS_ENDPOINT}"
        f"?q={quote_plus(query)}"
        f"&hl=en-US"
        f"&gl=US"
        f"&ceid=US:en"
    )

    r = session.get(
        url,
        timeout=REQUEST_TIMEOUT,
        headers={
            "User-Agent":
                "Mozilla/5.0 MacroWeb3RiskIntelligence/1.1"
        },
    )

    r.raise_for_status()

    root = ET.fromstring(r.content)

    out = []

    for item in root.findall(".//item")[:maxrecords]:

        title = (
            item.findtext("title") or ""
        ).strip()

        link = (
            item.findtext("link") or ""
        ).strip()

        pub = (
            item.findtext("pubDate") or ""
        ).strip()

        src = item.find("source")

        source_name = (
            (src.text or "").strip()
            if src is not None and src.text
            else ""
        )

        source_url = (
            (src.attrib.get("url") or "").strip()
            if src is not None
            else ""
        )

        if title and link:
            out.append(
                {
                    "url": link,
                    "title": title,
                    "seendate": pub,
                    "domain":
                        canonical_domain(source_url)
                        or canonical_domain(link),
                    "language": "English",
                    "sourcecountry": None,
                    "rss_source": source_name,
                }
            )

    return out


# ============================================================
# Domain Normalization
# ============================================================

def canonical_domain(url, fallback=""):
    try:
        return (
            urlparse(url)
            .netloc
            .lower()
            .removeprefix("www.")
            or fallback.lower()
        )
    except Exception:
        return fallback.lower()


# ============================================================
# Topic Classification
# ============================================================

def classify(text):
    s = text.lower()
    scored = []

    for topic, words in TOPICS.items():
        score = sum(
            1
            for w in words
            if w in s
        )

        if score:
            scored.append(
                (score, topic)
            )

    return (
        [
            topic
            for _, topic
            in sorted(
                scored,
                reverse=True,
            )
        ]
        or ["WEB3_RWA"]
    )


# ============================================================
# Freshness
# ============================================================

def freshness(dt, now):
    if not dt:
        return "UNKNOWN"

    age = now - dt

    if age <= timedelta(hours=36):
        return "FRESH"

    if age <= timedelta(days=7):
        return "STALE"

    return "ARCHIVED"


# ============================================================
# Stable News ID
# ============================================================

def item_id(url, title):
    return (
        "NEWS-"
        + hashlib.sha256(
            (
                url.strip()
                + "|"
                + title.strip()
            ).encode()
        ).hexdigest()[:12].upper()
    )


# ============================================================
# Explainability Context
# ============================================================

def build_context(topics):

    mapping = {
        "US_MACRO":
            "Macro policy and rates can affect liquidity, USD conditions, and cross-asset risk context.",

        "STABLECOIN":
            "Stablecoin developments can affect payment rails, on-chain liquidity, and institutional adoption.",

        "WEB3_RWA":
            "Web3/RWA developments can affect tokenization infrastructure and institutional on-chain adoption.",

        "DEFI":
            "DeFi developments can affect on-chain liquidity, credit, and protocol risk context.",

        "AGENTIC_AI":
            "Agentic finance developments are relevant to autonomous authorization and payment infrastructure.",

        "EXCHANGE":
            "Exchange developments can affect market access, liquidity, compliance, and infrastructure.",

        "TW_MARKET":
            "Taiwan market developments can affect semiconductor and cross-market risk context.",
    }

    return mapping.get(
        topics[0],
        mapping["WEB3_RWA"],
    )


# ============================================================
# P01 Context Linking
# ============================================================

def linked_context(topics):
    out = []

    if "US_MACRO" in topics:
        out += [
            "US10Y",
            "DXY",
            "MARKET_REGIME",
            "MARKET_RISK",
        ]

    if any(
        t in topics
        for t in (
            "WEB3_RWA",
            "STABLECOIN",
            "DEFI",
            "AGENTIC_AI",
            "EXCHANGE",
        )
    ):
        out += [
            "BTC",
            "ETH",
            "MARKET_REGIME",
            "EVIDENCE_CONFIDENCE",
        ]

    if "TW_MARKET" in topics:
        out += [
            "MARKET_REGIME",
            "MARKET_RISK",
        ]

    return list(
        dict.fromkeys(out)
    )


# ============================================================
# Article Normalization
# ============================================================

def normalize_article(
    raw,
    evidence_type,
    company,
    now,
    provider="GDELT",
):

    url = str(
        raw.get("url") or ""
    ).strip()

    title = str(
        raw.get("title") or ""
    ).strip()

    if not url or not title:
        return None

    published = parse_seen(
        raw.get("seendate")
    )

    domain = canonical_domain(
        url,
        str(
            raw.get("domain") or ""
        ),
    )

    topics = classify(
        " ".join(
            [
                title,
                company or "",
                domain,
            ]
        )
    )

    status = freshness(
        published,
        now,
    )

    return {
        "id":
            item_id(url, title),

        "title":
            title,

        "url":
            url,

        "domain":
            domain,

        "source_name":
            company
            or raw.get("rss_source")
            or domain
            or "Unknown source",

        "source_type":
            evidence_type,

        "provider":
            provider,

        "published_at":
            (
                published
                .isoformat()
                .replace("+00:00", "Z")
                if published
                else None
            ),

        "freshness":
            status,

        "language":
            raw.get("language"),

        "source_country":
            raw.get("sourcecountry"),

        "topics":
            topics,

        "primary_topic":
            topics[0],

        "why_it_matters":
            build_context(topics),

        "linked_p01_context":
            linked_context(topics),

        "evidence_note":
            (
                "Company-origin announcement; "
                "treat as first-party evidence."
                if evidence_type
                == "OFFICIAL_COMPANY_SOURCE"
                else
                "External news metadata; "
                "verify material claims at the original source."
            ),

        "limitations":
            (
                "Association with P01 context does not "
                "establish causality or constitute "
                "an investment recommendation."
            ),
    }


# ============================================================
# Deduplication
# ============================================================

def dedupe(items):
    seen = set()
    out = []

    for x in sorted(
        items,
        key=lambda a:
            a.get("published_at") or "",
        reverse=True,
    ):

        key = (
            (x.get("url") or "")
            .split("?")[0]
            .rstrip("/")
            .lower()
            or re.sub(
                r"\W+",
                " ",
                x.get(
                    "title",
                    "",
                ).lower(),
            ).strip()
        )

        titlekey = re.sub(
            r"\W+",
            " ",
            x.get(
                "title",
                "",
            ).lower(),
        ).strip()[:180]

        if (
            key in seen
            or ("title:" + titlekey)
            in seen
        ):
            continue

        seen.add(key)
        seen.add(
            "title:" + titlekey
        )

        out.append(x)

    return out


# ============================================================
# Fetch Individual Source
# ============================================================

def fetch_task(task, now):

    errors = []
    raws = []
    provider = "GDELT"

    gdelt_q = task.query

    if task.domains:
        gdelt_q = (
            f"("
            f"{' OR '.join('domain:' + d for d in task.domains)}"
            f") "
            f"({task.query})"
        )

    # --------------------------------------------------------
    # Primary: GDELT
    # --------------------------------------------------------

    try:
        raws = gdelt_query(
            gdelt_q,
            timespan=task.timespan,
            maxrecords=task.maxrecords,
        )

    except Exception as e:
        errors.append(
            {
                "source":
                    task.label,

                "provider":
                    "GDELT",

                "error":
                    str(e)[:300],
            }
        )

    # --------------------------------------------------------
    # Fallback: Google News RSS
    # --------------------------------------------------------

    if not raws:

        provider = "GOOGLE_NEWS_RSS"

        rss_q = task.query

        if task.domains:
            rss_q = (
                f"("
                f"{' OR '.join('site:' + d for d in task.domains)}"
                f") "
                f"{task.query}"
            )

        try:
            raws = google_news_query(
                rss_q,
                maxrecords=task.maxrecords,
            )

        except Exception as e:
            errors.append(
                {
                    "source":
                        task.label,

                    "provider":
                        "GOOGLE_NEWS_RSS",

                    "error":
                        str(e)[:300],
                }
            )

    evidence = (
        "OFFICIAL_COMPANY_SOURCE"
        if task.company
        else "NEWS_SOURCE"
    )

    items = []

    for raw in raws:

        # ----------------------------------------------------
        # Official-source allowlist verification
        # ----------------------------------------------------

        dom = str(
            raw.get("domain") or ""
        ).lower().removeprefix("www.")

        if (
            task.domains
            and dom
            and not any(
                dom == d
                or dom.endswith("." + d)
                for d in task.domains
            )
        ):
            continue

        x = normalize_article(
            raw,
            evidence,
            task.company,
            now,
            provider,
        )

        # ----------------------------------------------------
        # Only CURRENT-eligible freshness levels
        # ----------------------------------------------------

        if (
            x
            and x["freshness"]
            in {
                "FRESH",
                "STALE",
            }
        ):
            items.append(x)

    return (
        items,
        errors,
        {
            "source":
                task.label,

            "status":
                "OK"
                if items
                else "UNAVAILABLE",

            "items":
                len(items),

            "provider":
                provider,
        },
    )


# ============================================================
# Build Intelligence Feed
# ============================================================

def fetch_feed():

    now = datetime.now(
        timezone.utc
    )

    tasks = []

    # --------------------------------------------------------
    # General News Sources
    # --------------------------------------------------------

    for label, query in GENERAL_QUERIES.items():

        tasks.append(
            SourceTask(
                "NEWS:" + label,
                query,
                timespan="2d",
                maxrecords=50,
            )
        )

    # --------------------------------------------------------
    # Official / First-Party Sources
    # P01-NEWS-003:
    # Source-specific query selection
    # --------------------------------------------------------

    for company, domains in OFFICIAL_DOMAINS.items():

        query = OFFICIAL_QUERIES.get(
            company,
            (
                "blockchain crypto web3 "
                "stablecoin token payment "
                "DeFi RWA AI"
            ),
        )

        tasks.append(
            SourceTask(
                company,
                query,
                company,
                domains,
                "7d",
                30,
            )
        )

    items = []
    errors = []
    statuses = []

    # --------------------------------------------------------
    # Concurrent Fetch
    # --------------------------------------------------------

    with ThreadPoolExecutor(
        max_workers=MAX_WORKERS
    ) as ex:

        futures = {
            ex.submit(
                fetch_task,
                task,
                now,
            ): task
            for task in tasks
        }

        for future in as_completed(
            futures
        ):

            task = futures[future]

            try:
                i, e, s = future.result()

                items += i
                errors += e
                statuses.append(s)

            except Exception as exc:

                errors.append(
                    {
                        "source":
                            task.label,

                        "provider":
                            "INTERNAL",

                        "error":
                            str(exc)[:300],
                    }
                )

                statuses.append(
                    {
                        "source":
                            task.label,

                        "status":
                            "UNAVAILABLE",

                        "items":
                            0,

                        "provider":
                            "NONE",
                    }
                )

    # --------------------------------------------------------
    # Deduplicate + Sort
    # --------------------------------------------------------

    items = sorted(
        dedupe(items),
        key=lambda x: (
            x.get("published_at") or "",
            x["source_type"]
            == "OFFICIAL_COMPANY_SOURCE",
        ),
        reverse=True,
    )[:90]

    # --------------------------------------------------------
    # Final Feed
    # --------------------------------------------------------

    return {
        "schema_version":
            SCHEMA_VERSION,

        "engine":
            ENGINE,

        "generated_at":
            now_iso(),

        "status":
            "AVAILABLE"
            if items
            else "UNAVAILABLE",

        "sources":
            sorted(
                statuses,
                key=lambda x:
                    x["source"],
            ),

        "errors":
            errors,

        "items":
            items,

        "social_adapters": {
            "X":
                "NOT_CONFIGURED",

            "Threads":
                "PHASE_2",
        },

        "methodology": {
            "source_hierarchy": [
                "OFFICIAL_COMPANY_SOURCE",
                "NEWS_SOURCE",
                "SOCIAL_SIGNAL",
            ],

            "providers": [
                "GDELT_DOC_2.0",
                "GOOGLE_NEWS_RSS_FALLBACK",
            ],

            "freshness": {
                "FRESH":
                    "<=36h",

                "STALE":
                    "<=7d",

                "ARCHIVED":
                    ">7d",
            },

            "principles": [
                "Source provenance is explicit.",

                (
                    "First-party announcements "
                    "are not independent verification."
                ),

                (
                    "News-to-market matching is "
                    "contextual association, "
                    "not causal proof."
                ),

                "No investment recommendation.",
            ],
        },
    }


# ============================================================
# Validation
# ============================================================

def validate_feed(feed):

    assert (
        feed.get("schema_version")
        == SCHEMA_VERSION
    )

    assert (
        feed.get("engine")
        == ENGINE
    )

    assert (
        feed.get("status")
        in {
            "AVAILABLE",
            "UNAVAILABLE",
        }
    )

    assert isinstance(
        feed.get("items"),
        list,
    )

    for x in feed["items"]:

        for k in (
            "id",
            "title",
            "url",
            "source_name",
            "source_type",
            "freshness",
            "topics",
            "linked_p01_context",
            "limitations",
        ):
            assert k in x, k

        assert (
            x["source_type"]
            in {
                "OFFICIAL_COMPANY_SOURCE",
                "NEWS_SOURCE",
                "SOCIAL_SIGNAL",
            }
        )

        assert (
            x["freshness"]
            in {
                "FRESH",
                "STALE",
                "ARCHIVED",
                "UNKNOWN",
            }
        )

        assert x["url"].startswith(
            (
                "http://",
                "https://",
            )
        )


# ============================================================
# CLI
# ============================================================

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--output",
        default=
            "market_intelligence_feed.json",
    )

    parser.add_argument(
        "--strict",
        action="store_true",
    )

    args = parser.parse_args()

    feed = fetch_feed()

    validate_feed(feed)

    Path(
        args.output
    ).write_text(
        json.dumps(
            feed,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    ok = sum(
        1
        for source in feed["sources"]
        if source["status"] == "OK"
    )

    print(
        f"{ENGINE}: "
        f"{feed['status']} | "
        f"{len(feed['items'])} items | "
        f"{ok}/{len(feed['sources'])} sources available | "
        f"{len(feed['errors'])} provider errors"
    )

    if args.strict and (
        feed["status"] != "AVAILABLE"
        or not feed["items"]
        or ok < 1
    ):
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
