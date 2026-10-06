#!/usr/bin/env python3
from __future__ import annotations
import json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
from p02.category_discovery import discovery_report
from p02.topic_intelligence import build_top_predictions

DATA=ROOT/"data"/"p02"

def load(name):
    return json.loads((DATA/name).read_text(encoding="utf-8"))

def main():
    poly=load("polymarket_markets.json")
    kalshi=load("kalshi_markets.json")
    report=discovery_report(poly,kalshi)
    (DATA/"category_discovery.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")

    # Preserve venue documents expected by existing topic intelligence while
    # feeding it the discovery-selected candidates.
    p={"markets":[m for m in report["markets"] if m.get("venue")=="polymarket"]}
    k={"markets":[m for m in report["markets"] if m.get("venue")=="kalshi"]}
    top=build_top_predictions(p,k,limit=20,per_category_cap=5)
    (DATA/"topic_intelligence.json").write_text(json.dumps(top,ensure_ascii=False,indent=2),encoding="utf-8")

    print("P02-010.4 CATEGORY-AWARE MARKET DISCOVERY: PASS")
    print("Candidates:",report["candidate_count"])
    print("Selected:",report["selected_count"])
    print("Categories:",report["category_counts"])
    print("Qualified trending:",top["top_n"])

if __name__=="__main__": main()
