import json
from datetime import datetime,timezone
from pathlib import Path
from adapters import FredAdapter,MarketAdapter,CryptoAdapter
from adapters.base_adapter import BaseAdapter
EXPECTED_METRICS=("US10Y","DXY","VIX","BTC","ETH")

def err(mid,name,cat,unit,e): return BaseAdapter.result(mid,name,cat,unit,"Unavailable","NONE",status="ERROR",error=str(e))
def fetch_metric(mid):
    try:
        if mid=="US10Y":
            try: return FredAdapter().fetch(mid)
            except Exception as e:
                try:
                    x=MarketAdapter().fetch(mid); x["error"]=f"Primary FRED failed; fallback used: {e}"; return x
                except Exception as e2: return err(mid,"US 10-Year Treasury Yield","MACRO","%",f"FRED: {e}; yfinance: {e2}")
        if mid in ("DXY","VIX"): return MarketAdapter().fetch(mid)
        if mid in ("BTC","ETH"): return CryptoAdapter().fetch(mid)
    except Exception as e:
        meta={"DXY":("US Dollar Index","FX","INDEX"),"VIX":("CBOE Volatility Index","RISK","INDEX"),"BTC":("Bitcoin","CRYPTO","USD"),"ETH":("Ethereum","CRYPTO","USD")}
        n,c,u=meta[mid]; return err(mid,n,c,u,e)

def calculate_quality(metrics):
    c={"FRESH":0,"STALE":0,"MISSING":0,"ERROR":0}
    for m in EXPECTED_METRICS:
        if m not in metrics: c["MISSING"]+=1
        else: c[metrics[m].get("status","ERROR") if metrics[m].get("status") in c else "ERROR"]+=1
    fresh=c["FRESH"]; total=5; score=round(fresh/total,2)
    status="SUCCESS" if fresh==total else ("PARTIAL_SUCCESS" if fresh else "FAILED")
    return {"total":total,"fresh":fresh,"stale":c["STALE"],"missing":c["MISSING"],"error":c["ERROR"],"score":score,"status":status}

def main():
    start=datetime.now(timezone.utc); metrics={}
    print("P01-001 MULTI-SOURCE DATA ADAPTER PIPELINE")
    for m in EXPECTED_METRICS:
        metrics[m]=fetch_metric(m); x=metrics[m]
        print(f"{m}: {x['status']} | {x['source_type']} | {x['source']} | {x['value']}")
    q=calculate_quality(metrics); done=datetime.now(timezone.utc)
    Path("live_market_data.json").write_text(json.dumps({"schema_version":"1.0","generated_at":done.isoformat(),"metrics":metrics,"data_quality":q},ensure_ascii=False,indent=2),encoding="utf-8")
    Path("pipeline_status.json").write_text(json.dumps({"pipeline":"P01-001","started_at":start.isoformat(),"completed_at":done.isoformat(),"status":q["status"],"data_quality":q,"expected_metrics":list(EXPECTED_METRICS)},ensure_ascii=False,indent=2),encoding="utf-8")
    if q["fresh"]==0: raise RuntimeError("No expected metric returned FRESH data.")
if __name__=="__main__": main()
