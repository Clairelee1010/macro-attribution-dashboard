# INT-002 — Context Alignment & Divergence Engine

INT-002 connects P01 current-market context to P02 market-implied prediction contracts without turning context into causal proof, an outcome forecast, or a trading recommendation.

## Relationship states
- `SUPPORTED_CONTEXT` — P01 context is directionally consistent with the contract scenario.
- `DIVERGENT_CONTEXT` — P01 context points in a different direction from the contract scenario.
- `MIXED_CONTEXT` — relevant evidence is mixed.
- `INSUFFICIENT_EVIDENCE` — potentially relevant topic, but P01 evidence is not specific enough.
- `NOT_APPLICABLE` — intentionally outside P01 directional interpretation.

Political candidate/election contracts are always `NOT_APPLICABLE` to P01 directional inference. Their venue probability remains a market-implied observation only.

## Scope
INT-002 is deterministic and read-only. It does not emit BUY/SELL/LONG/SHORT/PAY/EXECUTE actions. `execution_allowed` remains `false`.

## Output
`data/integration/context_intelligence.json`

## Acceptance
Run:

```bash
pytest -q tests/integration/test_int001.py tests/integration/test_int002.py
python integration/integration_engine.py
python -m integration.context_intelligence_engine
```

Expected final label: `INT-002: PASS`.
