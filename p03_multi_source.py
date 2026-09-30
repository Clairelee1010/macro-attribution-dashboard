#!/usr/bin/env python3
"""P03-001A Multi-Source Public Market Data Collector.
Read-only public endpoints only. No account, order, wallet, signing, or fund execution code.
"""
from __future__ import annotations
import json, statistics, time
from datetime import datetime, timezone
from pathlib import Path
import requests
ROOT=Path(__file__).resolve().parent
REGISTRY=ROOT/'p03/data/exchange_registry.json'
OUT=ROOT/'p03/data/multi_source_market.json'
VALIDATION=ROOT/'p03/data/source_validation.json'
TIMEOUT=12
UA={'User-Agent':'ClaireLee-P03-Market-Intelligence/1.0','Accept':'application/json'}

def f(v):
    try:return float(v) if v not in (None,'') else None
    except (TypeError,ValueError):return None

def request_json(url,params=None):
    r=requests.get(url,params=params,headers=UA,timeout=TIMEOUT); r.raise_for_status(); return r.json()

def fetch(src,asset):
    sym=src['symbol_format'].format(base=asset)
    sid=src['id']; base=src['base_url']; ep=src['endpoint']
    if sid=='binance':
        d=request_json(base+ep,{'symbol':sym}); return d, {'price':f(d.get('lastPrice')),'bid':f(d.get('bidPrice')),'ask':f(d.get('askPrice')),'volume_24h':f(d.get('quoteVolume')),'source_ts':d.get('closeTime')}
    if sid=='mexc':
        d=request_json(base+ep,{'symbol':sym}); return d, {'price':f(d.get('lastPrice')),'bid':f(d.get('bidPrice')),'ask':f(d.get('askPrice')),'volume_24h':f(d.get('quoteVolume')),'source_ts':d.get('closeTime')}
    if sid=='gate':
        a=request_json(base+ep,{'currency_pair':sym}); d=a[0] if a else {}; return d, {'price':f(d.get('last')),'bid':f(d.get('highest_bid')),'ask':f(d.get('lowest_ask')),'volume_24h':f(d.get('quote_volume')),'source_ts':None}
    if sid=='bitget':
        a=request_json(base+ep,{'symbol':sym}); d=(a.get('data') or [{}])[0]; return d, {'price':f(d.get('lastPr')),'bid':f(d.get('bidPr')),'ask':f(d.get('askPr')),'volume_24h':f(d.get('quoteVolume')),'source_ts':d.get('ts') or a.get('requestTime')}
    if sid=='bybit':
        a=request_json(base+ep,{'category':'spot','symbol':sym}); d=((a.get('result') or {}).get('list') or [{}])[0]; return d, {'price':f(d.get('lastPrice')),'bid':f(d.get('bid1Price')),'ask':f(d.get('ask1Price')),'volume_24h':f(d.get('turnover24h')),'source_ts':a.get('time')}
    if sid=='coinbase':
        d=request_json(base+ep.replace('{symbol}',sym)); return d, {'price':f(d.get('price')),'bid':f(d.get('bid')),'ask':f(d.get('ask')),'volume_24h':f(d.get('volume')),'source_ts':d.get('time')}
    raise ValueError('unsupported source')

def iso_ts(v):
    if v is None:return None
    if isinstance(v,(int,float)) or (isinstance(v,str) and v.isdigit()):
        x=float(v); x=x/1000 if x>1e12 else x
        return datetime.fromtimestamp(x,tz=timezone.utc).isoformat()
    return str(v)

def main():
    cfg=json.loads(REGISTRY.read_text(encoding='utf-8')); now=datetime.now(timezone.utc).isoformat(); rows=[]
    for asset in cfg['assets']:
      for src in cfg['sources']:
        t=time.perf_counter()
        row={'asset':asset,'quote':cfg['quote'],'exchange':src['name'],'source_id':src['id'],'access':'PUBLIC_READ_ONLY','execution':'DISABLED','status':'UNAVAILABLE','collected_at':now}
        try:
          raw,n=fetch(src,asset); row.update(n); row['source_ts']=iso_ts(row.get('source_ts')); row['status']='AVAILABLE' if row.get('price') else 'INVALID'; row['latency_ms']=round((time.perf_counter()-t)*1000)
        except Exception as e:
          row['error']=f'{type(e).__name__}: {str(e)[:180]}'; row['latency_ms']=round((time.perf_counter()-t)*1000)
        rows.append(row)
    assets={}
    for asset in cfg['assets']:
      rs=[r for r in rows if r['asset']==asset]; ok=[r for r in rs if r['status']=='AVAILABLE' and r.get('price')]
      prices=[r['price'] for r in ok]; med=statistics.median(prices) if prices else None
      for r in ok:r['deviation_from_median_pct']=round((r['price']/med-1)*100,4) if med else None
      maxdev=max((abs(r['deviation_from_median_pct']) for r in ok),default=None)
      coverage=len(ok)/len(rs)*100 if rs else 0
      agreement='UNKNOWN' if len(ok)<2 else ('HIGH' if maxdev<=0.5 else 'MEDIUM' if maxdev<=1.5 else 'LOW')
      quality='FAIL' if not ok else ('PASS' if coverage>=80 and agreement in ('HIGH','MEDIUM') else 'DEGRADED')
      assets[asset]={'sources_checked':len(rs),'sources_available':len(ok),'evidence_coverage_pct':round(coverage,1),'median_price':med,'max_deviation_pct':maxdev,'source_agreement':agreement,'data_quality':quality}
    output={'version':'P03-001A','generated_at':now,'mode':'PUBLIC_READ_ONLY','execution':'DISABLED','guardrails':['NO_ACCOUNT','NO_ORDER','NO_WALLET','NO_SIGNING','NO_FUND_EXECUTION'],'assets':assets,'observations':rows}
    OUT.write_text(json.dumps(output,indent=2,ensure_ascii=False),encoding='utf-8')
    validation={'version':'P03-001A','generated_at':now,'overall_status':'PASS' if any(v['sources_available'] for v in assets.values()) else 'NO_LIVE_SOURCE','checks':assets,'execution':'DISABLED'}
    VALIDATION.write_text(json.dumps(validation,indent=2,ensure_ascii=False),encoding='utf-8')
    print('P03-001A',validation['overall_status']); [print(a,v) for a,v in assets.items()]
if __name__=='__main__':main()
