from pathlib import Path

HTML = Path("index.html").read_text(encoding="utf-8")

def test_product_title():
    assert "Macro & Web3 Risk Intelligence Engine" in HTML

def test_intelligence_contract():
    assert "dashboard_data.json" in HTML
    assert "live_market_data.json" in HTML

def test_executive_hooks():
    for hook in [
        "v5-regime", "v5-risk", "v5-confidence", "v5-quality",
        "v5-coverage", "v5-signals", "v5-drivers", "v5-evidence"
    ]:
        assert f'id="{hook}"' in HTML

def test_data_semantics():
    for value in ["LIVE", "GENERATED", "PROTOTYPE"]:
        assert value in HTML
    assert "data-semantics-note" in HTML

def test_provenance_and_freshness():
    assert 'id="live-provenance"' in HTML
    for state in ["FRESH", "STALE", "MISSING", "ERROR"]:
        assert state in HTML

def test_bilingual():
    assert "證據信心" in HTML
    assert "Evidence Confidence" in HTML
    assert "資料語意" in HTML
    assert "Data semantics" in HTML

def test_graceful_degradation():
    assert "stale analysis is not presented as current" in HTML
    assert "UNAVAILABLE" in HTML

def test_risk_confidence_semantics():
    assert "Risk ≠ confidence" in HTML
    assert "not market probability" in HTML
    assert "not causal proof" in HTML
