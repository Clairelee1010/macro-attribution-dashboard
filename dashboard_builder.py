import json
from pathlib import Path
from datetime import datetime, timezone

INPUTS = {
    "quality": "data_quality_report.json",
    "signals": "signal_report.json",
    "regime": "regime_report.json",
    "attribution": "attribution_report.json",
    "risk": "market_risk_report.json",
    "confidence": "confidence_evidence_report.json",
}

def _load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def build_dashboard_data(base_dir="."):
    base=Path(base_dir)
    d={k:_load(base/v) for k,v in INPUTS.items()}
    q,s,r,a,m,c=(d[x] for x in ("quality","signals","regime","attribution","risk","confidence"))
    generated=max(x.get("generated_at","") for x in d.values())
    return {
      "schema_version":"10.0", "engine":"P01-010", "generated_at":generated or datetime.now(timezone.utc).isoformat(),
      "executive_summary": {
        "market_regime":{"value":r["regime"],"score":r["score"],"confidence":r["confidence"],"coverage":r["coverage"]},
        "market_risk":{"level":m["risk_level"],"score":m["risk_score"],"confidence":m["confidence"],"evidence_coverage":m["evidence_coverage"]},
        "evidence_confidence":{"level":c["confidence_level"],"score":c["confidence_score"],"coverage":c["evidence_coverage"]},
        "data_quality":{"gate":q["quality_gate"],"score":q["quality_score"],"counts":q["counts"]}
      },
      "signals":s["signals"],
      "signal_summary":s["summary"],
      "attribution":{"confidence":a["attribution_confidence"],"agreement":a["evidence_agreement"],"drivers":a["drivers"],"excluded":a["excluded"]},
      "risk_drivers":m["risk_drivers"], "protective_factors":m["protective_factors"],
      "evidence":{"items":c["evidence"],"limitations":c["limitations"],"traceability":c["traceability"]},
      "semantics": {
        "risk":"Current deterministic market-risk assessment; not a forecast or recommendation.",
        "confidence":"Reliability of available supporting evidence; not causal or outcome probability.",
        "attribution":"Relative evidence alignment with the classified regime; not causal proof."
      }
    }

def write_dashboard_data(path="dashboard_data.json", base_dir="."):
    payload=build_dashboard_data(base_dir)
    Path(path).write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding="utf-8")
    return payload
