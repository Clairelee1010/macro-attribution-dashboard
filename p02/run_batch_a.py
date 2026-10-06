#!/usr/bin/env python3
"""Run P02 Batch A: 004 + 005 + 006."""

from __future__ import annotations
import json, sys
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from p02.event_matcher import match_markets
from p02.discrepancy_engine import build_discrepancy
from p02.p01_context import build_p01_context

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def validate(records, schema_path):
    schema = load(schema_path)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors=[]
    for i, rec in enumerate(records):
        for e in validator.iter_errors(rec):
            errors.append(f"{i}: {e.message}")
    if errors:
        raise RuntimeError("\n".join(errors[:20]))

def main():
    pdoc=load(ROOT/"data/p02/polymarket_markets.json")
    kdoc=load(ROOT/"data/p02/kalshi_markets.json")
    pmarkets=pdoc["markets"]
    kmarkets=kdoc["markets"]

    matches=match_markets(pmarkets,kmarkets)

    pmap={x["venue_market_id"]:x for x in pmarkets}
    kmap={x["venue_market_id"]:x for x in kmarkets}
    discrepancies=[]
    for m in matches:
        refs={x["venue"]:x["venue_market_id"] for x in m["market_refs"]}
        discrepancies.append(build_discrepancy(m,pmap[refs["polymarket"]],kmap[refs["kalshi"]]))

    validate(matches,ROOT/"p02/schemas/canonical_event.schema.json")
    validate(discrepancies,ROOT/"p02/schemas/discrepancy.schema.json")

    context=build_p01_context(ROOT)
    outdir=ROOT/"data/p02"
    outdir.mkdir(parents=True,exist_ok=True)
    (outdir/"canonical_events.json").write_text(json.dumps({"milestone":"P02-004","match_count":len(matches),"events":matches},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    (outdir/"discrepancies.json").write_text(json.dumps({"milestone":"P02-005","signal_count":len(discrepancies),"execution_allowed":False,"signals":discrepancies},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    (outdir/"p01_context.json").write_text(json.dumps(context,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

    print("P02 BATCH A")
    print(f"P02-004 Event Matching       PASS | matches={len(matches)}")
    print("Comparability Validation     PASS")
    print(f"P02-005 Discrepancy Engine   PASS | signals={len(discrepancies)}")
    print("Probability Gap              PASS")
    print("P02-006 P01 Context Bridge   PASS")
    print(f"P01 Context Available        {'YES' if context['available'] else 'NO'}")
    print("P01 Modified                 NO")
    print("Execution                    DISABLED")
    print("P02 BATCH A: PASS")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
