from datetime import datetime, timezone
import importlib.util
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[2] / "p02" / "adapters" / "polymarket_adapter.py"
spec = importlib.util.spec_from_file_location("polymarket_adapter", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(module)


def sample_market():
    return {
        "id": "123",
        "slug": "demo-market",
        "question": "Demo question?",
        "outcomes": '["Yes","No"]',
        "outcomePrices": '["0.62","0.38"]',
        "liquidity": "150248.32",
        "volume24hr": 5842.3,
        "bestBid": 0.61,
        "bestAsk": 0.63,
        "spread": 0.02,
        "startDateIso": "2026-09-01T00:00:00Z",
        "endDateIso": "2026-10-01T00:00:00Z",
    }


def test_yes_probability_from_gamma_arrays():
    assert module.yes_probability(sample_market()) == 0.62


def test_normalize_market():
    item = module.normalize_market(sample_market(), datetime(2026, 9, 25, tzinfo=timezone.utc))
    assert item["venue"] == "polymarket"
    assert item["venue_market_id"] == "123"
    assert item["implied_probability"] == 0.62
    assert item["volume_usd"] == 5842.3
    assert item["liquidity_usd"] == 150248.32
    assert item["best_bid"] == 0.61
    assert item["best_ask"] == 0.63
    assert item["spread"] == 0.02
    assert item["canonical_event"].startswith("UNMATCHED:")
    assert item["data_quality"] == "PASS"


def test_execution_is_not_part_of_market_record():
    item = module.normalize_market(sample_market(), datetime.now(timezone.utc))
    assert "execution_allowed" not in item
