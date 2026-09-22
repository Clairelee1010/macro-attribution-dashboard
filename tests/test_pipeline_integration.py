import json
from pathlib import Path
import update_market_data
def fake(m): return {"metric_id":m,"name":m,"category":"TEST","ticker":m,"value":1.0,"previous_close":.9,"change_pct":11.11,"unit":"INDEX","source":"Test","source_type":"PRIMARY","observed_at":"2026-09-22T00:00:00+00:00","fetched_at":"2026-09-22T00:01:00+00:00","status":"FRESH","error":None}
def test_outputs(monkeypatch,tmp_path):
    monkeypatch.chdir(tmp_path); monkeypatch.setattr(update_market_data,"fetch_metric",fake); update_market_data.main()
    d=json.loads(Path("live_market_data.json").read_text())
    assert d["schema_version"]=="1.0" and set(d["metrics"])==set(update_market_data.EXPECTED_METRICS) and d["data_quality"]["fresh"]==5
