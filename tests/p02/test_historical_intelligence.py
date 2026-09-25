import importlib.util
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]

def load_module(name, path):
    spec=importlib.util.spec_from_file_location(name, path)
    mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

snap=load_module("historical_snapshot", ROOT/"p02/historical_snapshot.py")
intel=load_module("historical_intelligence", ROOT/"p02/historical_intelligence.py")

def test_snapshot_semantics_and_execution_disabled():
    s=snap.build_snapshot("2026-09-26T00:00:00Z")
    assert s["milestone"]=="P02-009"
    assert s["execution_allowed"] is False
    assert "not a forecast" in s["semantics"]["probability"]

def test_baseline_only():
    s={"captured_at":"2026-09-26T00:00:00Z","markets":{"polymarket":[],"kalshi":[]},"discrepancies":[],"p01_context":{}}
    r=intel.build([s])
    assert r["snapshot_count"]==1
    assert r["history_state"]=="BASELINE_ONLY"
    assert r["execution_allowed"] is False

def test_probability_delta_is_percentage_points():
    a={"captured_at":"2026-09-25T00:00:00Z","markets":{"polymarket":[{"venue_market_id":"A","implied_probability":0.50}],"kalshi":[]},"discrepancies":[],"p01_context":{}}
    b={"captured_at":"2026-09-26T00:00:00Z","markets":{"polymarket":[{"venue_market_id":"A","implied_probability":0.57}],"kalshi":[]},"discrepancies":[],"p01_context":{}}
    r=intel.build([a,b])
    x=r["market_probability_changes"][0]
    assert x["probability_change_pp"]==7.0
    assert x["direction"]=="UP_STRONG"

def test_missing_previous_market_is_not_forced():
    a={"captured_at":"2026-09-25T00:00:00Z","markets":{"polymarket":[],"kalshi":[]},"discrepancies":[],"p01_context":{}}
    b={"captured_at":"2026-09-26T00:00:00Z","markets":{"polymarket":[{"venue_market_id":"NEW","implied_probability":0.60}],"kalshi":[]},"discrepancies":[],"p01_context":{}}
    r=intel.build([a,b])
    x=r["market_probability_changes"][0]
    assert x["previous_probability"] is None
    assert x["direction"]=="INSUFFICIENT_HISTORY"
