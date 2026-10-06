from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]

def read(p): return (ROOT/p).read_text(encoding="utf-8")

def test_design_scope_exists():
    for p in ["index.html","p02/index.html","intelligence/index.html"]:
        assert (ROOT/p).exists()
        assert "design-001-p01-alignment" in read(p)

def test_p02_soft_typography_override():
    s=read("p02/index.html")
    for token in [".brand{font-weight:500", ".engine-title,.section-title,.prediction-q,.question{font-weight:500", ".metric b,.summary b,.prediction-prob,.prob{font-weight:500"]:
        assert token in s

def test_integrated_soft_typography_override():
    s=read("intelligence/index.html")
    assert "h1{font-weight:500" in s
    assert ".big,.section h2,.value,.question,.prob{font-weight:500" in s

def test_home_and_p03_preview_alignment():
    s=read("index.html")
    assert "p03-preview" in s
    assert ".hero h1{font-weight:500" in s
    assert ".module.p03-preview h2{font-weight:500" in s

def test_p01_master_palette_reused():
    for p in ["index.html","p02/index.html","intelligence/index.html"]:
        s=read(p)
        assert "#fcfbf9" in s
        assert "#f0eae1" in s
