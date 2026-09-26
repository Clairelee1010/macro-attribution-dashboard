from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]

def read(p): return (ROOT/p).read_text(encoding="utf-8")

def test_routes_exist():
    for p in ["index.html","p01/index.html","p02/index.html","intelligence/index.html"]:
        assert (ROOT/p).exists(), p

def test_home_has_product_modules():
    s=read("index.html")
    for token in ["P01 · UNDERSTAND","P02 · PREDICT / COMPARE","INT-003 · CONTEXTUALIZE","P03 · GOVERN / ACT"]: assert token in s
    assert "Execution · DISABLED" in s

def test_shared_home_navigation():
    for p in ["p01/index.html","p02/index.html","intelligence/index.html"]:
        s=read(p)
        assert "Platform navigation" in s
        assert "P03 · Coming Soon" in s

def test_p01_moved_paths_are_safe():
    s=read("p01/index.html")
    for f in ["dashboard_data.json","market_intelligence_feed.json","live_market_data.json"]:
        assert f"../{f}" in s

def test_light_professional_typography():
    s=read("intelligence/index.html")
    assert "font-weight:850" not in s
    assert "font-weight:900" not in s
    assert "font-weight:600" in s
