#!/usr/bin/env python3
"""P02-006 — Read-only P01 context bridge.

P01 remains frozen. This module only reads existing generated P01 artifacts when present.
"""

from __future__ import annotations
import json
from pathlib import Path
from typing import Any

def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None

def build_p01_context(repo_root: Path) -> dict:
    regime = load_json(repo_root/"regime_report.json")
    signals = load_json(repo_root/"signal_report.json")
    pipeline = load_json(repo_root/"pipeline_status.json")

    available = any(x is not None for x in (regime, signals, pipeline))
    return {
        "bridge_version":"P02-006",
        "mode":"READ_ONLY",
        "p01_modified":False,
        "available":available,
        "regime_report":regime,
        "signal_report":signals,
        "pipeline_status":pipeline,
        "interpretation_rule":"P01 context is supporting evidence, not causal proof.",
    }
