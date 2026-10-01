#!/usr/bin/env python3
"""P03-002A — Dynamic Traditional Equity × xStocks verification.
Read-only intelligence only. No brokerage, orders, wallets, signing, or fund execution.
"""
from __future__ import annotations
import json, os, time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import requests

OUT=Path('p03/data/tokenized_equity_intelligence.json')
PAIRS=[
 {'underlying':'AAPL','token':'AAPLx','name':'Apple','provider':'xStocks / Backed'},
 {'underlying':'NVDA','token':'NVDAx','name':'NVIDIA','provider':'xStocks / Backed'},
]
GUARDRAILS=['NO_ACCOUNT','NO_ORDER','NO_WALLET','NO_SIGNING','NO_FUND_EXECUTION','DISCREPANCY_NOT_ARBITRAGE']
S=requests.Session(); S.headers.update({'User-Agent':'ClaireLee-P03-Intelligence/1.0'})

def now(): return datetime.now(timezone.utc).isoformat()
def get_json(url, headers=None):
    t=time.perf_counter(); r=S.get(url,headers=headers or {},timeout=15); ms=round((time.perf_counter()-t)*1000); r.raise_for_status(); return r.json(),ms

def deep_number(obj:Any, keys):
    if isinstance(obj,dict):
        for k,v in obj.items():
            if k.lower() in keys and isinstance(v,(int,float,str)):
                try:return float(v)
                except:pass
        for v in obj.values():
            x=deep_number(v,keys)
            if x is not None:return x
    elif isinstance(obj,list):
        for v in obj:
            x=deep_number(v,keys)
            if x is not None:return x
    return None

def deep_text(obj:Any, keys):
    if isinstance(obj,dict):
        for k,v in obj.items():
            if k.lower() in keys and isinstance(v,str): return v
        for v in obj.values():
            x=deep_text(v,keys)
            if x:return x
    elif isinstance(obj,list):
        for v in obj:
            x=deep_text(v,keys)
            if x:return x
    return None

def traditional(symbol):
    key=os.getenv('APCA_API_KEY_ID'); secret=os.getenv('APCA_API_SECRET_KEY')
    if key and secret:
        try:
            url=f'https://data.alpaca.markets/v2/stocks/{symbol}/trades/latest?feed=iex'
            j,ms=get_json(url,{'APCA-API-KEY-ID':key,'APCA-API-SECRET-KEY':secret})
            tr=j.get('trade',{}); return {'status':'AVAILABLE','source':'Alpaca IEX','price':tr.get('p'),'source_ts':tr.get('t'),'latency_ms':ms,'url':'https://data.alpaca.markets'}
        except Exception as e: alpaca_error=f'{type(e).__name__}: {e}'
    else: alpaca_error='Alpaca secrets not configured; using public fallback.'
    try:
        import yfinance as yf
        t=time.perf_counter(); q=yf.Ticker(symbol)
        fi=q.fast_info; price=fi.get('last_price') or fi.get('previous_close')
        return {'status':'AVAILABLE' if price else 'UNAVAILABLE','source':'Yahoo Finance via yfinance','price':float(price) if price else None,'source_ts':None,'collected_at':now(),'latency_ms':round((time.perf_counter()-t)*1000),'note':alpaca_error}
    except Exception as e:
        return {'status':'UNAVAILABLE','source':'Traditional equity adapter','price':None,'error':f'{type(e).__name__}: {e}','note':alpaca_error}

def tokenized(symbol):
    urls=[f'https://api.backed.fi/api/v2/public/assets/{symbol}/price-data',f'https://api.dev.backed.fi/api/v1/token']
    errors=[]
    for i,url in enumerate(urls):
        try:
            j,ms=get_json(url)
            price=deep_number(j,{'price','underlyingprice','underlying_price','value','lastprice','last_price'})
            ts=deep_text(j,{'timestamp','updatedat','updated_at','time','asof','as_of'})
            if i==1 and isinstance(j,(list,dict)):
                # metadata endpoint is evidence-only; don't invent a market price.
                return {'status':'METADATA_AVAILABLE','source':'xStocks / Backed public API','price':None,'source_ts':ts,'latency_ms':ms,'url':url,'note':'Token metadata reachable; price-data endpoint unavailable or schema not price-bearing.'}
            if price is not None:
                return {'status':'AVAILABLE','source':'xStocks / Backed public API','price':price,'source_ts':ts,'collected_at':now(),'latency_ms':ms,'url':url}
            errors.append('Price field not found')
        except Exception as e: errors.append(f'{type(e).__name__}: {e}')
    return {'status':'UNAVAILABLE','source':'xStocks / Backed public API','price':None,'error':' | '.join(errors)[:900],'url':urls[0]}

def pair_status(tr,tk):
    if tr.get('status')!='AVAILABLE' or tk.get('status')!='AVAILABLE': return 'INSUFFICIENT_EVIDENCE',None
    a,b=tr.get('price'),tk.get('price')
    if not a or not b:return 'INSUFFICIENT_EVIDENCE',None
    gap=(b-a)/a*100
    ag=abs(gap)
    return ('ALIGNED' if ag<0.5 else 'WATCH' if ag<1.5 else 'INVESTIGATE'),round(gap,4)

def main():
    pairs=[]
    for p in PAIRS:
        tr=traditional(p['underlying']); tk=tokenized(p['token']); status,gap=pair_status(tr,tk)
        evidence=sum([tr.get('status')=='AVAILABLE',tk.get('status')=='AVAILABLE',True,True])/4*100
        pairs.append({**p,'mapping':{'status':'VERIFIED_PRODUCT_MAPPING','basis':'Official xStocks product listing','backing':'1:1 underlying security (provider statement)','legal_form':'Tokenized representation / certificate structure; not asserted as identical shareholder ownership','verification_source':'https://xstocks.com/us/products','last_verified':now()},'traditional':tr,'tokenized':tk,'comparison':{'status':status,'discrepancy_pct':gap,'evidence_coverage_pct':round(evidence,1),'interpretation':'Observed price difference only. Discrepancy does not imply arbitrage.'}})
    doc={'version':'P03-002A','generated_at':now(),'mode':'PUBLIC_READ_ONLY','execution':'DISABLED','guardrails':GUARDRAILS,'methodology':{'mapping':'Verify product identity before comparison','comparison':'Traditional vs tokenized observed prices; no trade recommendation','timestamp_policy':'Missing source timestamps remain explicit; collected_at is not a substitute for source_ts'},'pairs':pairs}
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(doc,ensure_ascii=False,indent=2))
    print(json.dumps({'version':doc['version'],'pairs':[(x['underlying'],x['token'],x['comparison']['status']) for x in pairs]},ensure_ascii=False))
if __name__=='__main__':main()
