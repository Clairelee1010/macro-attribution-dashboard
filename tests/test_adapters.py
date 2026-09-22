from adapters.base_adapter import safe_number
from update_market_data import EXPECTED_METRICS,calculate_quality
def test_safe_number():
    assert safe_number("4.947")==4.947 and safe_number(None) is None
def test_fixed_denominator():
    q=calculate_quality({m:{"status":"FRESH"} for m in EXPECTED_METRICS[:-1]})
    assert q["total"]==5 and q["fresh"]==4 and q["missing"]==1 and q["score"]==0.8
