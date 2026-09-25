from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from p02.trust_security import aggregate_trust

def test_empty_security_feed_is_unknown_not_normal():
    r=aggregate_trust([])
    assert r["status"]=="UNKNOWN"
    assert "UNKNOWN_DOES_NOT_MEAN_SAFE" in r["limitations"]

def test_worst_evidence_status_wins():
    events=[
      {"status":"WATCH","evidence_state":"MULTI_SOURCE_REPORTED"},
      {"status":"ELEVATED","evidence_state":"OFFICIAL_CONFIRMED"},
    ]
    r=aggregate_trust(events)
    assert r["status"]=="ELEVATED"
    assert r["official_confirmed_count"]==1
