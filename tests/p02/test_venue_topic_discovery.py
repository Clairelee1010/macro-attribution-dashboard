from p02.venue_topic_discovery import polymarket_event_markets, select_kalshi_series
def test_polymarket_event_flatten_preserves_topic():
 ev=[{"id":"e1","_p02_discovery_topic":"crypto","markets":[{"id":"m1","question":"Will Bitcoin reach X?"}]}]
 rows=polymarket_event_markets(ev)
 assert len(rows)==1 and rows[0]["_p02_discovery_topic"]=="crypto"
def test_kalshi_series_uses_native_category_and_keywords():
 s=[
  {"ticker":"FED","title":"Federal Reserve decisions","category":"Economics","tags":["Fed"],"volume":100},
  {"ticker":"BTC","title":"Bitcoin prices","category":"Crypto","tags":["Bitcoin"],"volume":50},
  {"ticker":"NFL","title":"NFL games","category":"Sports","tags":["football"],"volume":999},
 ]
 rows=select_kalshi_series(s,per_topic=3)
 tickers={x["ticker"] for x in rows}
 assert "FED" in tickers and "BTC" in tickers and "NFL" not in tickers
