import json, importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location("eng",ROOT/"integration/integration_engine.py")
eng=importlib.util.module_from_spec(spec); spec.loader.exec_module(eng)
def test_int001_contract():
    d=eng.build_overview()
    assert d["version"]=="INT-001"
    assert d["execution_allowed"] is False
    assert d["architecture"]["p01"]=="UNDERSTAND"
    assert d["architecture"]["p02"]=="PREDICT_COMPARE"
    assert d["p01"]["regime"] in {"RISK_ON","NEUTRAL","RISK_OFF","UNKNOWN"}
    assert d["p02"]["ranked_predictions"] <= 20
    assert all(x["relationship"]=="INSUFFICIENT_EVIDENCE" for x in d["integrated_intelligence"])
def test_no_execution_language():
    d=eng.build_overview()
    s=json.dumps(d)
    assert '"execution_allowed": false' in s
