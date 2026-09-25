from p02.topic_intelligence import category_for, build_top_predictions

def market(i,q,venue="polymarket",volume=1000,liq=1000,p=.5):
    return {"event_id":f"{venue}:{i}","venue":venue,"question":q,"outcome":"YES","implied_probability":p,"volume_usd":volume,"liquidity_usd":liq,"market_close_time":None,"source_url":"https://example.com","retrieved_at":"2026-09-26T00:00:00Z","freshness":"FRESH","data_quality":"PASS"}

def test_topic_categories():
    assert category_for("Will Bitcoin reach $100k?")["key"]=="crypto"
    assert category_for("Will gold reach $5000?")["key"]=="metals"
    assert category_for("Will S&P 500 close above 7000?")["key"]=="equities"
    assert category_for("Will the NBA champion be Boston?")["key"]=="sports"

def test_dynamic_top20_and_cap():
    rows=[market(i,"Will Bitcoin reach a new level?",volume=100000-i) for i in range(10)]
    rows += [market(100+i,"Will gold reach a new level?",volume=90000-i) for i in range(10)]
    rows += [market(200+i,"Will S&P 500 close above a threshold?",volume=80000-i) for i in range(10)]
    out=build_top_predictions({"markets":rows},{"markets":[]},20,5)
    assert len(out["predictions"])==20
    assert out["predictions"][0]["rank"]==1
    assert all("category" in x and "trending_score" in x for x in out["predictions"])
