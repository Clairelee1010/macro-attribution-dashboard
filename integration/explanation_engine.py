from __future__ import annotations


def explain(prediction, p01, evaluation):
    category = prediction.get("category", {})
    key = category.get("key", "other") if isinstance(category, dict) else category
    state = evaluation["relationship"]
    scenario = evaluation["scenario"]

    if state == "NOT_APPLICABLE":
        if key == "politics":
            return "Candidate-specific political outcomes are intentionally not inferred from P01 macro context; the venue probability remains a market-implied observation only."
        return "This contract is outside the defined P01 market-context mapping and is intentionally not interpreted."

    if state == "INSUFFICIENT_EVIDENCE":
        return "The topic may be market-relevant, but current P01 evidence is not specific enough for a directional context comparison."

    if key == "macro":
        signals = [x.get("signal_id") for x in evaluation.get("evidence", []) if x.get("signal_id")]
        basis = ", ".join(signals) if signals else "available macro signals"
        if state == "SUPPORTED_CONTEXT":
            return f"The contract scenario ({scenario}) is directionally consistent with current P01 macro context ({basis}); this is context consistency, not causal proof or a forecast."
        if state == "DIVERGENT_CONTEXT":
            return f"The contract scenario ({scenario}) differs from the direction suggested by current P01 macro context ({basis}); this does not imply the market probability is wrong."
        return f"Current P01 macro evidence ({basis}) does not provide a single clean directional comparison for the contract scenario ({scenario})."

    if key == "crypto":
        regime = p01.get("regime", "UNKNOWN")
        if state == "SUPPORTED_CONTEXT":
            return f"The crypto scenario ({scenario}) is directionally consistent with the broad P01 regime ({regime}); asset-specific P01 evidence remains limited."
        if state == "DIVERGENT_CONTEXT":
            return f"The crypto scenario ({scenario}) differs from the broad P01 regime ({regime}); this is not a price forecast and asset-specific P01 evidence remains limited."

    return "Context relationship generated from deterministic INT-002 rules; no trading recommendation is produced."
