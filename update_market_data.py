import json
from datetime import datetime,timezone
from pathlib import Path
from adapters import FredAdapter,MarketAdapter,CryptoAdapter
from adapters.base_adapter import BaseAdapter
from schema_validation import validate_raw_payload
from normalization import normalize_payload
from normalization_validation import validate_normalized_payload
from data_quality import build_quality_report
from data_quality_validation import validate_data_quality_report
from signal_engine import build_signal_report
from signal_validation import validate_signal_report
from market_regime import build_regime_report
from regime_validation import validate_regime_report
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

    # P01-002 canonical raw-data envelope. Records preserve adapter provenance and
    # are validated before downstream consumers receive them.
    raw_payload={
        "schema_version":"2.0",
        "generated_at":done.isoformat(),
        "expected_metrics":list(EXPECTED_METRICS),
        "records":[metrics[m] for m in EXPECTED_METRICS],
    }
    validate_raw_payload(raw_payload)
    Path("raw_market_data.json").write_text(json.dumps(raw_payload,ensure_ascii=False,indent=2),encoding="utf-8")

    # P01-003 deterministic normalization layer. Raw values remain immutable and
    # every canonical value carries an explicit transformation lineage.
    normalized_payload=normalize_payload(raw_payload)
    validate_normalized_payload(normalized_payload)
    Path("normalized_market_data.json").write_text(json.dumps(normalized_payload,ensure_ascii=False,indent=2),encoding="utf-8")

    # P01-004 deterministic data quality layer. It evaluates whether normalized
    # observations are reliable enough for downstream intelligence.
    quality_report=build_quality_report(normalized_payload)
    validate_data_quality_report(quality_report)
    Path("data_quality_report.json").write_text(json.dumps(quality_report,ensure_ascii=False,indent=2),encoding="utf-8")

    # P01-005 deterministic signal layer. Only quality-eligible observations may
    # become descriptive market signals; this layer never emits trade recommendations.
    signal_report=build_signal_report(normalized_payload,quality_report)
    validate_signal_report(signal_report)
    Path("signal_report.json").write_text(json.dumps(signal_report,ensure_ascii=False,indent=2),encoding="utf-8")

    # P01-006 deterministic market regime layer. It aggregates eligible signals
    # while preserving contradictory evidence and excluding unknown signals.
    regime_report=build_regime_report(signal_report)
    validate_regime_report(regime_report)
    Path("regime_report.json").write_text(json.dumps(regime_report,ensure_ascii=False,indent=2),encoding="utf-8")

    # Backward-compatible v1.0 contract consumed by the current frontend.
    Path("live_market_data.json").write_text(json.dumps({"schema_version":"1.0","generated_at":done.isoformat(),"metrics":metrics,"data_quality":q},ensure_ascii=False,indent=2),encoding="utf-8")
    Path("pipeline_status.json").write_text(json.dumps({"pipeline":"P01-006","started_at":start.isoformat(),"completed_at":done.isoformat(),"status":q["status"],"data_quality":q,"expected_metrics":list(EXPECTED_METRICS),"raw_schema_version":"2.0","raw_schema_valid":True,"normalized_schema_version":"3.0","normalized_schema_valid":True,"data_quality_schema_version":"4.0","data_quality_schema_valid":True,"quality_gate":quality_report["quality_gate"],"quality_score":quality_report["quality_score"],"signal_schema_version":"5.0","signal_schema_valid":True,"signal_summary":signal_report["summary"],"regime_schema_version":"6.0","regime_schema_valid":True,"market_regime":regime_report["regime"],"regime_score":regime_report["score"],"regime_confidence":regime_report["confidence"]},ensure_ascii=False,indent=2),encoding="utf-8")
    if q["fresh"]==0: raise RuntimeError("No expected metric returned FRESH data.")
if __name__=="__main__": main()
