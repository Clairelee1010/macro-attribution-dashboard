import copy
import pytest
from normalization import normalize_record, normalize_payload
from normalization_validation import validate_normalized_payload


def raw(mid="US10Y", value=4.95, unit="%"):
    return {
        "metric_id": mid, "name": "name", "category": "MACRO", "ticker": "T",
        "value": value, "previous_close": 4.9, "change_pct": 1.0, "unit": unit,
        "source": "source", "source_type": "PRIMARY",
        "observed_at": "2026-09-22T00:00:00+00:00", "fetched_at": "2026-09-22T01:00:00+00:00",
        "status": "FRESH", "error": None,
    }


def test_us10y_percent_to_decimal():
    out = normalize_record(raw())
    assert out["raw"] == {"value": 4.95, "unit": "%"}
    assert out["normalized"]["value"] == 0.0495
    assert out["normalized"]["unit"] == "DECIMAL"
    assert out["transformation"]["type"] == "PERCENT_TO_DECIMAL"


def test_identity_crypto():
    r = raw("BTC", 86273.7579, "USD")
    r["category"] = "CRYPTO"
    out = normalize_record(r)
    assert out["normalized"]["value"] == 86273.7579
    assert out["transformation"]["type"] == "IDENTITY"


def test_unknown_metric_rejected():
    with pytest.raises(ValueError):
        normalize_record(raw("UNKNOWN", 1, "INDEX"))


def test_null_value_preserved_for_error():
    r = raw("VIX", None, "INDEX")
    r["category"] = "RISK"; r["status"] = "ERROR"; r["error"] = "boom"; r["observed_at"] = None
    out = normalize_record(r)
    assert out["raw"]["value"] is None
    assert out["normalized"]["value"] is None


def test_payload_schema_and_lineage():
    rows=[]
    for mid, val, unit, cat in [("US10Y",4.95,"%","MACRO"),("DXY",100.2,"INDEX","FX"),("VIX",15.2,"INDEX","RISK"),("BTC",86000,"USD","CRYPTO"),("ETH",2700,"USD","CRYPTO")]:
        r=raw(mid,val,unit); r["category"]=cat; rows.append(r)
    payload=normalize_payload({"schema_version":"2.0","generated_at":"2026-09-22T01:00:00+00:00","expected_metrics":[r["metric_id"] for r in rows],"records":rows})
    assert validate_normalized_payload(payload)
    assert payload["schema_version"] == "3.0"
    assert payload["source_schema_version"] == "2.0"
    assert len(payload["records"]) == 5
