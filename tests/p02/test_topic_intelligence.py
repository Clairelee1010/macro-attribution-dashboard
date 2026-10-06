from p02.topic_intelligence import category_for, build_top_predictions

def market(i,q,venue="polymarket",volume=1000,liq=1000,p=.5):
    return {"event_id":f"{venue}:{i}","venue":venue,"question":q,"outcome":"YES",
            "implied_probability":p,"volume_usd":volume,"liquidity_usd":liq,
            "market_close_time":None,"source_url":"https://example.com",
            "retrieved_at":"2026-09-26T00:00:00Z","freshness":"FRESH","data_quality":"PASS"}

def test_topic_categories():
    assert category_for("Will Bitcoin reach $100k?")["key"]=="crypto"
    assert category_for("Will gold reach $5000?")["key"]=="metals"
    assert category_for("Will S&P 500 close above 7000?")["key"]=="equities"
    assert category_for("Will the NBA champion be Boston?")["key"]=="sports"
    assert category_for("Will the Fed cut rates in December?")["key"]=="macro"
    assert category_for("Will CPI exceed 3%?")["key"]=="macro"
    assert category_for("Will the Democratic presidential nominee win?")["key"]=="politics"

def test_no_crypto_substring_collision():
    # Regression: ETH in Kenneth previously caused a false Crypto label.
    assert category_for("Will Kenneth Walker III record 85+ rushing yards?")["key"]=="sports"
    assert category_for("Will Pete Hegseth win the 2028 US Presidential Election?")["key"]=="politics"

def test_dynamic_top20_and_cap():
    rows=[market(i,"Will Bitcoin reach a new level?",volume=100000-i) for i in range(10)]
    rows += [market(100+i,"Will gold reach a new level?",volume=90000-i) for i in range(10)]
    rows += [market(200+i,"Will S&P 500 close above a threshold?",volume=80000-i) for i in range(10)]
    rows += [market(300+i,"Will the Fed cut rates?",volume=70000-i) for i in range(10)]
    out=build_top_predictions({"markets":rows},{"markets":[]},20,5)
    assert len(out["predictions"])==20
    assert out["predictions"][0]["rank"]==1
    assert out["ranking_method"]=="DETERMINISTIC_RELEVANCE_V3_QUALITY_GATED"
    assert all("category" in x and "trending_score" in x for x in out["predictions"])
    assert max(out["category_counts"].values()) <= 5


def test_quality_gate_rejects_parlay_and_zero_information():
    good = market(1, "Will Bitcoin reach $100k?", volume=50000, liq=20000, p=.55)
    parlay = market(2, "yes USA,yes France,yes Netherlands,yes Over 1.5 goals scored", venue="kalshi", volume=0, liq=0, p=0)
    out = build_top_predictions({"markets":[good]},{"markets":[parlay]},20,5)
    assert len(out["predictions"]) == 1
    assert out["predictions"][0]["question"] == good["question"]
    assert out["quality_policy"] == "UP_TO_20_NO_FORCED_FILL"

def test_no_forced_fill_beyond_category_cap():
    rows=[market(i,f"Will candidate {i} win the presidential election?",volume=100000-i,liq=10000,p=.2) for i in range(12)]
    out=build_top_predictions({"markets":rows},{"markets":[]},20,5)
    assert len(out["predictions"]) == 5
    assert out["category_counts"]["politics"] == 5

def test_pete_hegseth_is_politics():
    assert category_for("Will Pete Hegseth win the 2028 US Presidential Election?")["key"] == "politics"
