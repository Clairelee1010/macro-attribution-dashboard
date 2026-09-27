"""INT-004 Cross-Market Trend Intelligence.

Read-only context artifact. Fetches 30-day daily history for cross-market context.
It does not alter P01 signals/regime/risk and does not generate forecasts or trades.
"""
from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path
import requests
import yfinance as yf

OUT = Path('data/integration/cross_market_trends.json')
MARKETS = {
    'US10Y': {'name':'US 10Y Treasury Yield','ticker':'^TNX','unit':'%','group':'Macro','source':'Yahoo Finance via yfinance'},
    'DXY': {'name':'US Dollar Index','ticker':'DX-Y.NYB','unit':'INDEX','group':'FX','source':'Yahoo Finance via yfinance'},
    'VIX': {'name':'CBOE Volatility Index','ticker':'^VIX','unit':'INDEX','group':'Risk','source':'Yahoo Finance via yfinance'},
    'SP500': {'name':'S&P 500','ticker':'^GSPC','unit':'INDEX','group':'Equity','source':'Yahoo Finance via yfinance'},
}
CRYPTO = {
    'BTC': {'id':'bitcoin','name':'Bitcoin','unit':'USD','group':'Crypto','source':'CoinGecko Public API'},
    'ETH': {'id':'ethereum','name':'Ethereum','unit':'USD','group':'Crypto','source':'CoinGecko Public API'},
}

def _change(values, days):
    if len(values) <= days or values[-1] in (None,0) or values[-1-days] in (None,0): return None
    return round((values[-1]/values[-1-days]-1)*100, 2)

def _series(metric_id, meta, rows):
    rows=[(d,float(v)) for d,v in rows if v is not None]
    values=[v for _,v in rows]
    if not rows:
        return {'metric_id':metric_id, **{k:meta[k] for k in ('name','unit','group','source')}, 'status':'UNAVAILABLE','points':[]}
    base=values[0]
    points=[{'date':d,'value':round(v,6),'indexed':round(v/base*100,4) if base else None} for d,v in rows]
    return {'metric_id':metric_id, **{k:meta[k] for k in ('name','unit','group','source')},
            'status':'LIVE' if len(points)>=7 else 'INSUFFICIENT_HISTORY', 'current':round(values[-1],6),
            'change_1d_pct':_change(values,1), 'change_7d_pct':_change(values,7),
            'change_30d_pct':_change(values,min(30,len(values)-1)) if len(values)>1 else None, 'points':points}

def fetch_yf(mid, meta):
    h=yf.Ticker(meta['ticker']).history(period='1mo',interval='1d',auto_adjust=False)
    c=h['Close'].dropna()
    rows=[]
    for idx,val in c.items(): rows.append((idx.strftime('%Y-%m-%d'), float(val)))
    return _series(mid,meta,rows)

def fetch_crypto(mid, meta):
    r=requests.get(f"https://api.coingecko.com/api/v3/coins/{meta['id']}/market_chart", params={'vs_currency':'usd','days':'30','interval':'daily'}, timeout=20)
    r.raise_for_status(); prices=r.json().get('prices',[])
    rows=[]
    for ts,val in prices:
        d=datetime.fromtimestamp(ts/1000,tz=timezone.utc).strftime('%Y-%m-%d')
        if rows and rows[-1][0]==d: rows[-1]=(d,float(val))
        else: rows.append((d,float(val)))
    return _series(mid,meta,rows)

def main():
    series=[]
    for mid,meta in MARKETS.items():
        try: series.append(fetch_yf(mid,meta))
        except Exception as e: series.append({'metric_id':mid,'name':meta['name'],'unit':meta['unit'],'group':meta['group'],'source':meta['source'],'status':'UNAVAILABLE','error':str(e),'points':[]})
    for mid,meta in CRYPTO.items():
        try: series.append(fetch_crypto(mid,meta))
        except Exception as e: series.append({'metric_id':mid,'name':meta['name'],'unit':meta['unit'],'group':meta['group'],'source':meta['source'],'status':'UNAVAILABLE','error':str(e),'points':[]})
    payload={'product':'Cross-Market Trend Intelligence','version':'INT-004','generated_at':datetime.now(timezone.utc).isoformat(),
             'methodology':{'chart':'Indexed performance; first available point = 100','purpose':'Cross-market context only','forecast':False,'execution_allowed':False},
             'series':series}
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8')
    print('INT-004:', ', '.join(f"{x['metric_id']}={x['status']}" for x in series))
if __name__=='__main__': main()
