"""INT-005A Multi-Asset Market Watchlist.
Representative, transparent market universe; not a popularity ranking or recommendation.
Read-only market context. No forecasts, scores, recommendations, or execution.
"""
from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path
import yfinance as yf

OUT=Path('data/integration/multi_asset_watchlist.json')
ASSETS=[
('AAPL','Apple','US Equity','Technology'),('MSFT','Microsoft','US Equity','Technology'),('NVDA','NVIDIA','US Equity','Technology'),('AMZN','Amazon','US Equity','Consumer'),('GOOGL','Alphabet','US Equity','Communication'),('META','Meta Platforms','US Equity','Communication'),('TSLA','Tesla','US Equity','Consumer'),('AVGO','Broadcom','US Equity','Technology'),('JPM','JPMorgan Chase','US Equity','Financials'),('BRK-B','Berkshire Hathaway','US Equity','Financials'),('LLY','Eli Lilly','US Equity','Healthcare'),('WMT','Walmart','US Equity','Consumer'),('XOM','Exxon Mobil','US Equity','Energy'),('V','Visa','US Equity','Financials'),('NFLX','Netflix','US Equity','Communication'),
('SPY','SPDR S&P 500 ETF','ETF','Broad Market'),('QQQ','Invesco QQQ','ETF','Nasdaq 100'),('IVV','iShares Core S&P 500 ETF','ETF','Broad Market'),('IWM','iShares Russell 2000 ETF','ETF','Small Cap'),('VTI','Vanguard Total Stock Market ETF','ETF','Broad Market'),('DIA','SPDR Dow Jones Industrial Average ETF','ETF','Dow 30'),
('SHY','iShares 1-3 Year Treasury Bond ETF','US Treasury','Short Duration'),('IEF','iShares 7-10 Year Treasury Bond ETF','US Treasury','Intermediate Duration'),('TLT','iShares 20+ Year Treasury Bond ETF','US Treasury','Long Duration'),('BIL','SPDR Bloomberg 1-3 Month T-Bill ETF','US Treasury','T-Bills'),
('GLD','SPDR Gold Shares','Gold','Gold ETF'),('IAU','iShares Gold Trust','Gold','Gold ETF'),
('BTC-USD','Bitcoin','Crypto','Crypto'),('ETH-USD','Ethereum','Crypto','Crypto'),('SOL-USD','Solana','Crypto','Crypto')]

def pct(a,b):
    if a is None or b in (None,0): return None
    return round((a/b-1)*100,2)

def fetch(symbol,name,asset_class,sector):
    h=yf.Ticker(symbol).history(period='1mo',interval='1d',auto_adjust=False)['Close'].dropna()
    vals=[float(x) for x in h.tolist()]
    dates=[x.strftime('%Y-%m-%d') for x in h.index]
    if not vals: raise ValueError('no price history')
    return {'symbol':symbol.replace('-USD',''),'ticker':symbol,'name':name,'asset_class':asset_class,'sector':sector,'status':'LIVE' if len(vals)>=7 else 'INSUFFICIENT_HISTORY','current':round(vals[-1],6),'change_1d_pct':pct(vals[-1],vals[-2]) if len(vals)>1 else None,'change_7d_pct':pct(vals[-1],vals[-8]) if len(vals)>7 else None,'change_30d_pct':pct(vals[-1],vals[0]) if len(vals)>1 else None,'currency':'USD','source':'Yahoo Finance via yfinance','points':[{'date':d,'value':round(v,6)} for d,v in zip(dates,vals)]}

def main():
    rows=[]
    for a in ASSETS:
        try: rows.append(fetch(*a))
        except Exception as e: rows.append({'symbol':a[0].replace('-USD',''),'ticker':a[0],'name':a[1],'asset_class':a[2],'sector':a[3],'status':'UNAVAILABLE','source':'Yahoo Finance via yfinance','error':str(e),'points':[]})
    payload={'product':'Multi-Asset Market Watchlist','version':'INT-005A','generated_at':datetime.now(timezone.utc).isoformat(),'methodology':{'universe':'30 representative assets across US equities, ETFs, US Treasury ETFs, gold ETFs and crypto. This is not a popularity ranking, investment ranking, or recommendation.','ranking':False,'forecast':False,'execution_allowed':False},'assets':rows}
    OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8')
    print('INT-005A:',sum(x['status']!='UNAVAILABLE' for x in rows),'/',len(rows),'available')
if __name__=='__main__': main()
