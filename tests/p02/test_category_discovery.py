from p02.category_discovery import discover_balanced, discovery_report

def m(i,q,venue="polymarket",v=1000,l=500):
    return {"event_id":str(i),"venue":venue,"question":q,"volume_usd":v,
            "liquidity_usd":l,"freshness":"FRESH","data_quality":"PASS",
            "implied_probability":.5}

def test_category_aware_selection_preserves_diversity():
    rows=[]
    for i in range(20): rows.append(m(i,f"Will candidate {i} win the presidential election?",v=100000-i))
    for i in range(4): rows.append(m(100+i,f"Will Bitcoin reach target {i}?",v=100+i))
    for i in range(3): rows.append(m(200+i,f"Will gold reach target {i}?",v=100+i))
    selected,counts=discover_balanced(rows,per_category=5,total_limit=12)
    assert counts["politics"] >= 5
    assert counts["crypto"] == 4
    assert counts["metals"] == 3
    assert len(selected)==12

def test_no_relabeling_or_execution():
    poly={"markets":[m(1,"Will the Fed cut rates?")]}
    kalshi={"markets":[m(2,"Will an NBA team win?",venue="kalshi")]}
    r=discovery_report(poly,kalshi,5,10)
    assert r["category_counts"]["macro"]==1
    assert r["category_counts"]["sports"]==1
    assert r["execution_allowed"] is False
    assert r["markets"][0]["question"] in {"Will the Fed cut rates?","Will an NBA team win?"}
