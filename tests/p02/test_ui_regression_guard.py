from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def test_p02_published_and_source_are_top6():
    for rel in ["p02/index.html", "p02-web/index.html"]:
        h = (ROOT / rel).read_text(encoding="utf-8")
        assert "rows=rows.slice(0,6);" in h
        assert "Dynamic Top 6" in h
        assert "Trending Top 20" not in h

def test_p02_source_and_published_match():
    assert (ROOT / "p02/index.html").read_text(encoding="utf-8") == (ROOT / "p02-web/index.html").read_text(encoding="utf-8")
