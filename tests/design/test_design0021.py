from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
P01 = (ROOT / "p01" / "index.html").read_text(encoding="utf-8")


def test_p01_product_navigation_zh():
    for label in ["市場情報", "預測情報", "整合情報", "Agent 治理"]:
        assert label in P01


def test_p01_product_navigation_en():
    for label in ["Home", "Market", "Prediction", "Integrated", "Agent Governance"]:
        assert label in P01


def test_technical_version_badge_preserved():
    assert "P01 v1.0 · NEWS-005" in P01


def test_routes_preserved():
    for route in ['href="../"', 'href="./"', 'href="../p02/"', 'href="../intelligence/"']:
        assert route in P01


def test_old_engineering_nav_removed():
    assert '>P01</a>' not in P01
    assert '>P02</a>' not in P01
    assert 'P03 · Coming Soon</span>' not in P01
