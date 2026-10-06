import requests,yfinance as yf
from datetime import datetime,timezone
from .base_adapter import BaseAdapter,safe_number

class CryptoAdapter(BaseAdapter):
    CFG={"BTC":("bitcoin","BTC-USD","Bitcoin"),"ETH":("ethereum","ETH-USD","Ethereum")}
    def fetch(self,metric_id):
        if metric_id not in self.CFG: raise KeyError(metric_id)
        try: return self.retry(lambda:self._cg(metric_id))
        except Exception as e:
            x=self.retry(lambda:self._yf(metric_id)); x["error"]=f"Primary CoinGecko failed; fallback used: {e}"; return x
    def _cg(self,m):
        cid,ticker,name=self.CFG[m]
        r=requests.get(f"https://api.coingecko.com/api/v3/coins/{cid}/market_chart",params={"vs_currency":"usd","days":"2","interval":"daily"},timeout=15); r.raise_for_status()
        p=r.json().get("prices",[])
        if not p: raise ValueError("No CoinGecko prices")
        ts,raw=p[-1]; cur=safe_number(raw); prev=safe_number(p[-2][1]) if len(p)>1 else None
        obs=datetime.fromtimestamp(ts/1000,tz=timezone.utc); age=(datetime.now(timezone.utc)-obs).total_seconds()/3600
        ch=round((cur-prev)/prev*100,2) if prev not in (None,0) else None
        return self.result(m,name,"CRYPTO","USD","CoinGecko Public API","PRIMARY",ticker,cur,prev,ch,obs.isoformat(),"FRESH" if age<=48 else "STALE")
    def _yf(self,m):
        _,ticker,name=self.CFG[m]; c=yf.Ticker(ticker).history(period="5d",interval="1d",auto_adjust=False)["Close"].dropna()
        if c.empty: raise ValueError("No fallback data")
        cur=safe_number(c.iloc[-1]); prev=safe_number(c.iloc[-2]) if len(c)>1 else None; obs=c.index[-1]
        if obs.tzinfo is None: obs=obs.tz_localize("UTC")
        obs=obs.tz_convert("UTC"); ch=round((cur-prev)/prev*100,2) if prev not in (None,0) else None
        return self.result(m,name,"CRYPTO","USD","Yahoo Finance via yfinance","FALLBACK",ticker,cur,prev,ch,obs.isoformat(),"FRESH")
