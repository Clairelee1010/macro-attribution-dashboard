import json
from pathlib import Path
DEFAULT_RULES_PATH=Path(__file__).resolve().parent/"config"/"market_risk_rules.json"
def load_market_risk_rules(path=None):
    path=Path(path) if path is not None else DEFAULT_RULES_PATH
    return json.loads(path.read_text(encoding="utf-8"))
def _level(score,levels):
    if score<float(levels["LOW"]["max_exclusive"]): return "LOW"
    if score<float(levels["MODERATE"]["max_exclusive"]): return "MODERATE"
    return "HIGH"
def build_market_risk_report(a,rules=None):
    rules=rules or load_market_risk_rules(); cfg=rules["score"]; regime=a.get("regime","UNKNOWN")
    score=float(cfg["base"])+float(cfg["regime_adjustment"].get(regime,cfg["regime_adjustment"]["UNKNOWN"]))
    risk=[]; protective=[]
    for d in a.get("drivers",[]):
        direction=d.get("direction","UNKNOWN"); share=float(d.get("contribution_share",0)); conf=float(d.get("signal_confidence",0))
        impact=share*conf*float(cfg["driver_weight"])
        item={"metric_id":d["metric_id"],"signal_id":d.get("signal_id"),"direction":direction,"strength":d.get("strength","UNKNOWN"),"contribution_share":round(share,4),"signal_confidence":round(conf,4),"risk_impact":round(abs(impact),4)}
        if direction=="RISK_OFF": score+=impact; risk.append(item)
        elif direction=="RISK_ON": score-=impact; protective.append(item)
    eligible=int(a.get("summary",{}).get("eligible_drivers",len(a.get("drivers",[]))))
    excluded=int(a.get("summary",{}).get("excluded_signals",0)); denom=eligible+excluded
    coverage=round(eligible/denom,4) if denom else 0.0
    upstream=float(a.get("attribution_confidence",0))
    if upstream<0.5: score+=float(cfg["low_confidence_penalty"])*(1-upstream)
    if coverage<0.8: score+=float(cfg["low_coverage_penalty"])*(1-coverage)
    score=round(max(0,min(100,score)),2)
    confidence=round(max(0,min(1,upstream*coverage)),4)
    if regime=="UNKNOWN": confidence=min(confidence,float(rules["confidence"]["unknown_regime_cap"]))
    risk.sort(key=lambda x:(-x["risk_impact"],x["metric_id"])); protective.sort(key=lambda x:(-x["risk_impact"],x["metric_id"]))
    return {"schema_version":"8.0","source_schema_version":a["schema_version"],"generated_at":a["generated_at"],"engine":"P01-008","rules_version":rules["version"],"regime":regime,"risk_score":score,"risk_level":_level(score,rules["levels"]),"confidence":confidence,"evidence_coverage":coverage,"risk_drivers":risk,"protective_factors":protective,"excluded":a.get("excluded",[]),"summary":{"risk_driver_count":len(risk),"protective_factor_count":len(protective),"eligible_drivers":eligible,"excluded_signals":excluded},"semantics":rules["semantics"]}
