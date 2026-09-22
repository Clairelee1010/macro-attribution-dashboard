import yfinance as yf
from datetime import datetime,timezone
from .base_adapter import BaseAdapter,safe_number

class MarketAdapter(BaseAdapter):
    CFG={"US10Y":("^TNX","US 10-Year Treasury Yield","MACRO","%","FALLBACK"),"DXY":("DX-Y.NYB","US Dollar Index","FX","INDEX","PRIMARY"),"VIX":("^VIX","CBOE Volatility Index","RISK","INDEX","PRIMARY")}
    def fetch(self,metric_id):
        if metric_id not in self.CFG: raise KeyError(metric_id)
        ticker,name,cat,unit,stype=self.CFG[metric_id]
        def op():
            h=yf.Ticker(ticker).history(period="5d",interval="1d",auto_adjust=False)
            c=h["Close"].dropna()
            if c.empty: raise ValueError("No market data")
            cur=safe_number(c.iloc[-1]); prev=safe_number(c.iloc[-2]) if len(c)>1 else None
            obs=c.index[-1]
            if obs.tzinfo is None: obs=obs.tz_localize("UTC")
            obs=obs.tz_convert("UTC")
            age=(datetime.now(timezone.utc)-obs.to_pydatetime()).total_seconds()/86400
            ch=round((cur-prev)/prev*100,2) if prev not in (None,0) else None
            return self.result(metric_id,name,cat,unit,"Yahoo Finance via yfinance",stype,ticker,cur,prev,ch,obs.isoformat(),"FRESH" if age<=5 else "STALE")
        return self.retry(op)
