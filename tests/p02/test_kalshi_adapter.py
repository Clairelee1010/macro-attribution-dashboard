from datetime import datetime, timezone
import importlib.util
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[2] / "p02" / "adapters" / "kalshi_adapter.py"
spec = importlib.util.spec_from_file_location("kalshi_adapter", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(module)


def sample_market():
    return {
        "ticker": "DEMO-FED",
        "title": "Will the demo event occur?",
        "last_price_dollars": "0.5500",
        "yes_bid_dollars": "0.5400",
        "yes_ask_dollars": "0.5600",
        "volume_24h_fp": "12345.00",
        "open_interest_fp": "45678.00",
        "open_time": "2026-09-01T00:00:00Z",
        "close_time": "2026-10-01T00:00:00Z",
        "rules_primary": "Demo rule.",
    }


def test_probability_prefers_fixed_point_dollars():
    assert module.implied_yes_probability(sample_market()) == 0.55


def test_normalize_market():
    item = module.normalize_market(sample_market(), datetime(2026, 9, 25, tzinfo=timezone.utc))
    assert item["venue"] == "kalshi"
    assert item["venue_market_id"] == "DEMO-FED"
    assert item["implied_probability"] == 0.55
    assert item["best_bid"] == 0.54
    assert item["best_ask"] == 0.56
    assert round(item["spread"], 4) == 0.02
    assert item["canonical_event"].startswith("UNMATCHED:")
    assert item["data_quality"] == "PASS"


def test_legacy_cents_fallback():
    market = {"last_price": 63}
    assert module.implied_yes_probability(market) == 0.63
