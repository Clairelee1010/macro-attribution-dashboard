from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))

from p02.event_matcher import lexical_similarity, comparability_label, match_markets
from p02.discrepancy_engine import build_discrepancy
from p02.p01_context import build_p01_context

def market(venue,id,q,p):
    return {
        "venue":venue,"venue_market_id":id,"question":q,"implied_probability":p,
        "market_close_time":"2026-10-31T00:00:00Z","freshness":"FRESH","data_quality":"PASS"
    }

def test_similarity():
    assert lexical_similarity("Will CPI be above 3 percent?", "Will CPI exceed 3 percent?") > 0.4

def test_match_and_discrepancy():
    p=market("polymarket","p1","Will CPI be above 3 percent? ",0.62)
    k=market("kalshi","k1","Will CPI be above 3 percent?",0.55)
    matches=match_markets([p],[k])
    assert len(matches)==1
    d=build_discrepancy(matches[0],p,k)
    assert d["raw_discrepancy_pp"]==7.0
    assert d["execution_allowed"] is False

def test_unrelated_not_matched():
    p=market("polymarket","p1","Will CPI be above 3 percent?",0.62)
    k=market("kalshi","k1","Will a baseball team win tonight?",0.55)
    assert match_markets([p],[k])==[]

def test_p01_bridge_is_read_only():
    c=build_p01_context(ROOT)
    assert c["mode"]=="READ_ONLY"
    assert c["p01_modified"] is False
