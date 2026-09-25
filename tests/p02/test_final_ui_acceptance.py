import json
from pathlib import Path
def test_ui_release_badge_and_coverage_semantics():
    h=Path("p02-web/index.html").read_text(encoding="utf-8")
    assert "P02 v1.0 · PRODUCTION" in h
    assert "discovery_category_counts" in h
    assert "Discovery coverage ≠ Trending selection" in h
    assert "沒有市場通過 Trending Top 20 排名" in h
def test_builder_exports_discovery_counts():
    s=Path("p02/build_dashboard_payload.py").read_text(encoding="utf-8")
    assert 'topic_intelligence["discovery_category_counts"]' in s
    assert 'topic_intelligence["discovery_candidate_count"]' in s
    assert '"version":"P02-v1.0"' in s
