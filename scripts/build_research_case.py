"""Freeze a supplied snapshot; never invent probabilities or cross-venue matches.
Run manually only when deliberately publishing a new dated case study.
"""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads((ROOT/p).read_text())
paths=['live_market_data.json','regime_report.json','data/p02/topic_intelligence.json','data/p02/canonical_events.json','data/p02/kalshi_markets.json']
docs={p:read(p) for p in paths}
archive=ROOT/'research/evidence'
archive.mkdir(exist_ok=True)
for p in paths: (archive/Path(p).name).write_bytes((ROOT/p).read_bytes())
contracts=[x for x in docs[paths[2]].get('predictions',[]) if 'October 2026 meeting' in x.get('question','') and 'Fed' in x['question']]
case={
 'id':'fomc-october-2026','type':'FROZEN_RESEARCH_SNAPSHOT','snapshot_at':docs[paths[0]].get('generated_at'),
 'event':{'title_zh':'2026 年 10 月 FOMC：利率預期與宏觀風險','title_en':'October 2026 FOMC: rate expectations and macro risk','meeting_dates':['2026-10-27','2026-10-28'],'official_url':'https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm','calendar_checked_on':'2026-10-16','calendar_scope':'Meeting dates verified against the Federal Reserve calendar. This does not verify exchange contract rules or prices.'},
 'macro':docs[paths[0]],'regime':docs[paths[1]],'contracts':contracts,
 'comparison':{'status':'WITHHELD','verified_pairs':0,'reasons':['NO_VERIFIED_COUNTERPART_IN_THIS_SNAPSHOT','RESOLUTION_RULES_ABSENT_FROM_TOPIC_ROWS','RAW_FEEDS_AND_TOPIC_DISCOVERY_HAVE_DIFFERENT_COVERAGE'],'scanned_kalshi_rows':len(docs[paths[4]].get('markets',[])),'warning':'Zero verified pairs is not evidence that no counterpart exists on either venue. No price-gap or arbitrage conclusion is published.'},
 'provenance':[{'path':p,'archive_path':'research/evidence/'+Path(p).name,'sha256':hashlib.sha256((ROOT/p).read_bytes()).hexdigest()} for p in paths],
 'authenticity':'Values copied from user-supplied repository artifacts. Retrieval timestamps are not exchange quote timestamps; prices and contract rules have not been independently revalidated against exchanges.',
 'method':'Rule-based context and human-authored research framing; no Gemini output is stored in this case.'
}
(ROOT/'research/case-study.json').write_text(json.dumps(case,ensure_ascii=False,indent=2)+'\n')
print(f'Frozen case: {len(contracts)} supplied contracts; no fabricated counterpart.')
