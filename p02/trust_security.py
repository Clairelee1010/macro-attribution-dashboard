#!/usr/bin/env python3
"""P02-007 Trust & Security Intelligence.

Deterministic trust-status aggregation from normalized security events.
No incident is invented: an empty event set returns UNKNOWN.
"""
from __future__ import annotations
from typing import Any

SEVERITY = {"NORMAL":0, "UNKNOWN":1, "WATCH":2, "ELEVATED":3, "CRITICAL":4}

def aggregate_trust(events: list[dict[str, Any]]) -> dict[str, Any]:
    if not events:
        return {
            "status":"UNKNOWN",
            "event_count":0,
            "official_confirmed_count":0,
            "reasons":["NO_SECURITY_EVENT_FEED_CONFIGURED"],
            "limitations":["UNKNOWN_DOES_NOT_MEAN_SAFE","NO_INCIDENT_IS_INFERRED_FROM_ABSENCE_OF_DATA"],
        }

    worst = max(events, key=lambda e: SEVERITY.get(e.get("status","UNKNOWN"),1))
    official = sum(e.get("evidence_state")=="OFFICIAL_CONFIRMED" for e in events)
    return {
        "status":worst.get("status","UNKNOWN"),
        "event_count":len(events),
        "official_confirmed_count":official,
        "reasons":[f"HIGHEST_EVENT_STATUS_{worst.get('status','UNKNOWN')}"],
        "limitations":["SECURITY_STATUS_IS_EVIDENCE_BASED_NOT_A_GUARANTEE"],
    }
