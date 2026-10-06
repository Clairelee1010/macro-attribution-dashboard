from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]

def read(path): return (ROOT / path).read_text(encoding='utf-8')

def test_home_uses_product_names():
    s=read('index.html')
    assert 'data-i18n="marketNav">市場情報</a>' in s
    assert 'data-i18n="predictionNav">預測情報</a>' in s
    assert 'data-i18n="agentNav">Agent 治理</span>' in s
    assert 'MARKET INTELLIGENCE · UNDERSTAND' in s
    assert 'PREDICTION INTELLIGENCE · PREDICT / COMPARE' in s
    assert 'INTEGRATED INTELLIGENCE · CONTEXTUALIZE' in s
    assert 'AGENT GOVERNANCE · GOVERN / ACT' in s

def test_shared_navigation_uses_product_names():
    for f in ['p01/index.html','p02/index.html','intelligence/index.html']:
        s=read(f)
        assert '>市場情報</a>' in s
        assert '>預測情報</a>' in s
        assert '>整合情報</a>' in s
        assert 'Agent 治理 · Coming Soon' in s

def test_home_ctas_are_product_facing():
    s=read('index.html')
    assert '探索市場情報 →' in s
    assert '探索預測情報 →' in s
    assert "enterP01:'Explore Market Intelligence →'" in s
    assert "enterP02:'Explore Prediction Intelligence →'" in s

def test_internal_version_identifiers_preserved():
    assert 'P01 v1.0 · NEWS-005' in read('p01/index.html')
    assert 'P02 v1.0' in read('p02/index.html')

def test_routes_unchanged():
    s=read('index.html')
    for route in ['./p01/','./p02/','./intelligence/']:
        assert route in s
