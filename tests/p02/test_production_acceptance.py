import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def load_module():
    p = ROOT / "p02" / "production_acceptance.py"
    spec = importlib.util.spec_from_file_location("production_acceptance", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def test_acceptance_semantics_are_conservative():
    mod = load_module()
    result = mod.run_acceptance()
    assert result["semantics"]["zero_matches_is_valid"] is True
    assert result["semantics"]["probability_is_observation_not_forecast"] is True
    assert result["semantics"]["discrepancy_is_not_arbitrage"] is True
    assert result["semantics"]["trust_unknown_is_not_safe"] is True
    assert result["semantics"]["execution_allowed"] is False

def test_p01_is_read_only_context():
    mod = load_module()
    result = mod.run_acceptance()
    assert result["checks"]["p01_read_only_context"] is True
    assert result["checks"]["execution_disabled"] is True

def test_production_acceptance_passes():
    mod = load_module()
    result = mod.run_acceptance()
    assert result["status"] == "PASS"
    assert result["release_state"] == "READY_TO_FREEZE"
