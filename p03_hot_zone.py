#!/usr/bin/env python3
"""P03-003A Hot Zone Intelligence.
Evidence-first market attention heat. This is NOT a fund-flow or trading engine.
Uses existing generated artifacts only and never fabricates missing capital-flow data.
"""
from __future__ import annotations
import json, math
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'p03/data/hot_zone_intelligence.json'

def load(rel):
    p=ROOT/rel
    return json.loads(p.read_text(encoding='utf-8')) if p.exists() else None

def clamp(v,a=0,b=100): return max(a,min(b,v))
def momentum_heat(change):
    # absolute activity/momentum, not direction or attractiveness
    if change is None: return None
    return round(clamp(38 + min(abs(float(change))*5.2,42)),1)

def level(s):
    if s is None: return 'INSUFFICIENT_EVIDENCE'
    return 'VERY_HOT' if s>=78 else 'HOT' if s>=64 else 'WATCH' if s>=48 else 'COOL'

def avg(vals):
    vals=[v for v in vals if v is not None]
    return sum(vals)/len(vals) if vals else None

cross=load('data/integration/cross_market_trends.json') or {}
watch=load('data/integration/multi_asset_watchlist.json') or {}
topics=load('data/p02/topic_intelligence.json') or {}
mapping=load('data/integration/tokenization_mapping.json') or {}
eq=load('p03/data/tokenized_equity_intelligence.json') or {}

series={x.get('metric_id'):x for x in cross.get('series',[])}
assets={x.get('symbol'):x for x in watch.get('assets',[])}
preds=topics.get('predictions',[])
verified=[m for m in mapping.get('mappings',[]) if m.get('status')=='VERIFIED']
verified_symbols={m.get('symbol') for m in verified}

windows={'24H':'change_1d_pct','7D':'change_7d_pct','30D':'change_30d_pct'}
zones=[]

def market_zone(zid,zh,en,symbol,kind='MARKET_MOMENTUM'):
    src=assets.get(symbol) or series.get(symbol) or {}
    scores={w:momentum_heat(src.get(k)) for w,k in windows.items()}
    changes={w:src.get(k) for w,k in windows.items()}
    zones.append({'id':zid,'name_zh':zh,'name_en':en,'evidence_type':'OBSERVED_MARKET_DATA','heat_basis':kind,
      'scores':scores,'levels':{w:level(s) for w,s in scores.items()},'changes_pct':changes,
      'evidence_coverage_pct':100.0 if src else 0.0,'source':src.get('source','Cross-Market Trend Intelligence'),
      'note_zh':'熱度反映價格活動／動能強度，不代表資金淨流入或投資建議。','note_en':'Heat reflects market activity/momentum, not net capital inflow or investment advice.'})

market_zone('BTC','比特幣','Bitcoin','BTC')
market_zone('ETH','以太坊','Ethereum','ETH')
market_zone('SOL','Solana','Solana','SOL')

# US equity attention: aggregate live watchlist momentum; direction retained separately.
equities=[x for x in assets.values() if x.get('asset_class')=='US Equity' and x.get('status')=='LIVE']
if equities:
    sc={}; ch={}
    for w,k in windows.items():
        vals=[x.get(k) for x in equities if x.get(k) is not None]
        ch[w]=round(avg(vals),2) if vals else None
        sc[w]=round(avg([momentum_heat(v) for v in vals]),1) if vals else None
    zones.append({'id':'US_EQUITY','name_zh':'美股觀察池','name_en':'US Equity Watchlist','evidence_type':'OBSERVED_MARKET_DATA','heat_basis':'AGGREGATE_WATCHLIST_MOMENTUM','scores':sc,'levels':{w:level(v) for w,v in sc.items()},'changes_pct':ch,'evidence_coverage_pct':100.0,'source':'INT multi-asset watchlist','note_zh':'以觀察池價格活動聚合，不代表整體美股資金流。','note_en':'Aggregated watchlist activity; not whole-market fund flow.'})

# Tokenized equity: structure/mapping evidence + underlying activity; explicitly inferred attention, not flow.
under=[assets[s] for s in verified_symbols if s in assets and assets[s].get('status')=='LIVE']
map_cov=round(100*len(verified)/max(1,len(mapping.get('mappings',[]))),1) if mapping.get('mappings') else 0
if verified:
    sc={}; ch={}
    for w,k in windows.items():
        vals=[x.get(k) for x in under if x.get(k) is not None]
        ch[w]=round(avg(vals),2) if vals else None
        base=avg([momentum_heat(v) for v in vals])
        sc[w]=round(clamp((base or 35)*.72 + min(len(verified)*2.2,20)),1)
    zones.append({'id':'TOKENIZED_EQUITY','name_zh':'代幣化股票','name_en':'Tokenized Equities','evidence_type':'INFERRED_ATTENTION','heat_basis':'VERIFIED_MAPPING_PLUS_UNDERLYING_ACTIVITY','scores':sc,'levels':{w:level(v) for w,v in sc.items()},'changes_pct':ch,'evidence_coverage_pct':map_cov,'source':'INT verified tokenization mapping + live underlying watchlist','note_zh':'推論型熱度：結合已驗證產品映射與標的市場活動；不是代幣資金淨流入。','note_en':'Inferred heat combines verified product mappings and underlying activity; it is not token net inflow.'})

# Prediction market attention uses current volume/liquidity/trending; no political outcome direction is used.
nonpolit=[p for p in preds if (p.get('category') or {}).get('key')!='politics']
if nonpolit:
    top=nonpolit[:10]
    trend=avg([p.get('trending_score') for p in top if p.get('trending_score') is not None]) or 0
    vol=sum(float(p.get('volume_usd') or 0) for p in top)
    liq=sum(float(p.get('liquidity_usd') or 0) for p in top)
    score=round(clamp(.72*trend + min(math.log10(max(vol,1))*2.2,18)),1)
    zones.append({'id':'PREDICTION','name_zh':'預測市場注意力','name_en':'Prediction Market Attention','evidence_type':'OBSERVED_MARKET_ACTIVITY','heat_basis':'NON_POLITICAL_TRENDING_VOLUME_LIQUIDITY','scores':{'24H':score,'7D':score,'30D':score},'levels':{'24H':level(score),'7D':level(score),'30D':level(score)},'changes_pct':{'24H':None,'7D':None,'30D':None},'evidence_coverage_pct':100.0,'source':'P02 deterministic topic intelligence','activity':{'top_nonpolitical_markets':len(top),'volume_usd':round(vol,2),'liquidity_usd':round(liq,2)},'note_zh':'僅衡量非政治市場的活動與注意力，不預測事件結果。','note_en':'Measures non-political market activity/attention only; it does not predict outcomes.'})

# RWA placeholder: preserve unknown rather than inventing a flow number.
zones.append({'id':'RWA','name_zh':'RWA / 鏈上實體資產','name_en':'RWA / Tokenized Real-World Assets','evidence_type':'INSUFFICIENT_DIRECT_FLOW_EVIDENCE','heat_basis':'DIRECT_FLOW_SOURCE_REQUIRED','scores':{'24H':None,'7D':None,'30D':None},'levels':{'24H':'EVIDENCE_PENDING','7D':'EVIDENCE_PENDING','30D':'EVIDENCE_PENDING'},'changes_pct':{'24H':None,'7D':None,'30D':None},'evidence_coverage_pct':0.0,'source':None,'note_zh':'目前 Repo 沒有可驗證的直接 RWA 淨流資料，因此不建立假熱度。','note_en':'No verified direct RWA net-flow source is present in the repo, so no synthetic heat is created.'})

# Relationships are contextual/inferred only. No claim that money literally moved between nodes.
flows=[
 {'from':'US_EQUITY','to':'TOKENIZED_EQUITY','type':'CONTEXT_LINK','strength':62,'observed':False,'label_zh':'標的市場 ↔ 代幣化映射','label_en':'Underlying ↔ tokenized mapping'},
 {'from':'BTC','to':'ETH','type':'MARKET_ROTATION_CONTEXT','strength':48,'observed':False,'label_zh':'跨加密市場活動比較','label_en':'Cross-crypto activity comparison'},
 {'from':'ETH','to':'RWA','type':'EVIDENCE_PENDING','strength':22,'observed':False,'label_zh':'等待直接資金流證據','label_en':'Direct flow evidence pending'}]

out={'version':'P03-003A','generated_at':datetime.now(timezone.utc).isoformat(),'mode':'PUBLIC_READ_ONLY','execution':'DISABLED',
 'guardrails':['NO_ACCOUNT','NO_ORDER','NO_WALLET','NO_SIGNING','NO_FUND_EXECUTION','HEAT_NOT_RECOMMENDATION','ATTENTION_NOT_CAPITAL_FLOW','INFERRED_FLOW_LABELED'],
 'methodology':{'heat_score':'Deterministic attention/activity score from existing verified artifacts; score is investigation priority, not investment attractiveness.','flow_policy':'Only direct net-flow evidence may be labeled OBSERVED_FLOW. Context links are labeled inferred/contextual.','politics':'Political prediction-market contracts are excluded from Hot Zone scoring.'},
 'zones':zones,'flows':flows}
OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print('P03-003A hot-zone intelligence written:',OUT)
