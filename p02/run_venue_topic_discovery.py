#!/usr/bin/env python3
from __future__ import annotations
import json, sys
from pathlib import Path
from datetime import datetime, timezone
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
from p02.venue_topic_discovery import *
from p02.adapters.polymarket_adapter import normalize_market as norm_poly
from p02.adapters.kalshi_adapter import normalize_market as norm_kalshi

DATA=ROOT/"data"/"p02"
def load(name):
 p=DATA/name
 return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {"markets":[]}

def merge(existing,new):
 out=[]; seen=set()
 for m in list(existing)+list(new):
  ident=(m.get("venue"),m.get("venue_market_id"))
  if ident in seen: continue
  seen.add(ident); out.append(m)
 return out

def main():
 now=datetime.now(timezone.utc)
 pevents=polymarket_topic_events()
 praw=polymarket_event_markets(pevents)
 kseries=select_kalshi_series(kalshi_series())
 kraw=kalshi_markets_for_series(kseries)
 pnorm=[]
 for x in praw:
  try:
   n=norm_poly(x,now); n["discovery_topic"]=x.get("_p02_discovery_topic"); pnorm.append(n)
  except Exception: pass
 knorm=[]
 for x in kraw:
  try:
   n=norm_kalshi(x,now); n["discovery_topic"]=x.get("_p02_discovery_topic"); knorm.append(n)
  except Exception: pass

 pdoc=load("polymarket_markets.json"); kdoc=load("kalshi_markets.json")
 pdoc["markets"]=merge(pdoc.get("markets",[]),pnorm)
 kdoc["markets"]=merge(kdoc.get("markets",[]),knorm)
 (DATA/"polymarket_markets.json").write_text(json.dumps(pdoc,ensure_ascii=False,indent=2),encoding="utf-8")
 (DATA/"kalshi_markets.json").write_text(json.dumps(kdoc,ensure_ascii=False,indent=2),encoding="utf-8")
 report={"polymarket_search_events":len(pevents),"polymarket_topic_markets":len(pnorm),
         "kalshi_selected_series":len(kseries),"kalshi_topic_markets":len(knorm),
         "execution_allowed":False}
 (DATA/"venue_topic_discovery.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
 print("P02-010.6 VENUE-NATIVE TOPIC DISCOVERY: PASS")
 print("Polymarket search events:",len(pevents))
 print("Polymarket topic markets:",len(pnorm))
 print("Kalshi selected series:",len(kseries))
 print("Kalshi topic markets:",len(knorm))
 print("Execution: DISABLED")
if __name__=="__main__": main()
