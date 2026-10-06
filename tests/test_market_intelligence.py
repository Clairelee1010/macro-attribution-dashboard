import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from datetime import datetime, timezone, timedelta
import market_intelligence as mi

def test_classification_and_context():
    topics=mi.classify("Circle launches USDC stablecoin payments for AI agent x402")
    assert "STABLECOIN" in topics and "AGENTIC_AI" in topics
    ctx=mi.linked_context(topics)
    assert "BTC" in ctx and "EVIDENCE_CONFIDENCE" in ctx

def test_normalize_official_source():
    now=datetime(2026,9,24,2,0,tzinfo=timezone.utc)
    raw={"url":"https://www.circle.com/blog/example","title":"USDC payment update","seendate":"20260924T010000Z","domain":"circle.com","language":"English","sourcecountry":"United States"}
    item=mi.normalize_article(raw,evidence_type="OFFICIAL_COMPANY_SOURCE",company="Circle",now=now)
    assert item["freshness"]=="FRESH"
    assert item["source_type"]=="OFFICIAL_COMPANY_SOURCE"
    assert "first-party" in item["evidence_note"]

def test_dedupe():
    base={"published_at":"2026-09-24T01:00:00Z","title":"A"}
    out=mi.dedupe([{**base,"url":"https://x.test/a?utm=1"},{**base,"url":"https://x.test/a"}])
    assert len(out)==1

def test_bootstrap_contract():
    feed=json.loads(Path("market_intelligence_feed.json").read_text())
    mi.validate_feed(feed)

def test_frontend_has_no_legacy_recommendation_or_execution_labels():
    html=Path("index.html").read_text(encoding="utf-8")
    assert "RECOMMENDED US EQUITIES" not in html
    assert "Soft Robi Execution Log:" not in html
    assert "market_intelligence_feed.json" in html
    assert "OFFICIAL_COMPANY_SOURCE" in html
