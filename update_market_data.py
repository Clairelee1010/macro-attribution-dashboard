import json
import math
from datetime import datetime, timezone

import yfinance as yf


# ============================================================
# P01-000B — Live Market Data Pipeline v1
# Purpose:
#   Fetch live market data without requiring local Python.
#   Designed to run inside GitHub Actions.
# ============================================================

MARKET_METRICS = {
    "US10Y": {
        "ticker": "^TNX",
        "name": "US 10-Year Treasury Yield",
        "category": "MACRO",
        "unit": "%"
    },
    "DXY": {
        "ticker": "DX-Y.NYB",
        "name": "US Dollar Index",
        "category": "FX",
        "unit": "INDEX"
    },
    "VIX": {
        "ticker": "^VIX",
        "name": "CBOE Volatility Index",
        "category": "RISK",
        "unit": "INDEX"
    },
    "BTC": {
        "ticker": "BTC-USD",
        "name": "Bitcoin",
        "category": "CRYPTO",
        "unit": "USD"
    },
    "ETH": {
        "ticker": "ETH-USD",
        "name": "Ethereum",
        "category": "CRYPTO",
        "unit": "USD"
    }
}


def safe_number(value):
    """Convert market values into JSON-safe numbers."""
    try:
        number = float(value)

        if math.isnan(number) or math.isinf(number):
            return None

        return round(number, 4)

    except (TypeError, ValueError):
        return None


def fetch_metric(metric_id, config):

    fetched_at = datetime.now(timezone.utc).isoformat()

    result = {
        "metric_id": metric_id,
        "name": config["name"],
        "category": config["category"],
        "ticker": config["ticker"],
        "value": None,
        "previous_close": None,
        "change_pct": None,
        "unit": config["unit"],
        "source": "Yahoo Finance via yfinance",
        "observed_at": None,
        "fetched_at": fetched_at,
        "status": "ERROR",
        "error": None
    }

    try:

        ticker = yf.Ticker(config["ticker"])

        history = ticker.history(
            period="5d",
            interval="1d",
            auto_adjust=False
        )

        if history.empty:
            raise ValueError("No market data returned")

        closes = history["Close"].dropna()

        if closes.empty:
            raise ValueError("Close price unavailable")

        current = safe_number(closes.iloc[-1])

        previous = (
            safe_number(closes.iloc[-2])
            if len(closes) >= 2
            else None
        )

        change_pct = None

        if (
            current is not None
            and previous not in (None, 0)
        ):
            change_pct = round(
                ((current - previous) / previous) * 100,
                2
            )

        result["value"] = current
        result["previous_close"] = previous
        result["change_pct"] = change_pct
        result["observed_at"] = (
            closes.index[-1].isoformat()
        )
        result["status"] = "FRESH"

    except Exception as exc:

        result["error"] = str(exc)

    return result


def calculate_quality(metrics):

    total = len(metrics)

    fresh = sum(
        1 for metric in metrics.values()
        if metric["status"] == "FRESH"
    )

    errors = sum(
        1 for metric in metrics.values()
        if metric["status"] == "ERROR"
    )

    score = round(fresh / total, 2) if total else 0

    if fresh == total:
        pipeline_status = "SUCCESS"

    elif fresh > 0:
        pipeline_status = "PARTIAL_SUCCESS"

    else:
        pipeline_status = "FAILED"

    return {
        "total": total,
        "fresh": fresh,
        "stale": 0,
        "error": errors,
        "score": score,
        "status": pipeline_status
    }


def main():

    started_at = datetime.now(timezone.utc)

    print("=" * 60)
    print("P01-000B LIVE MARKET DATA PIPELINE")
    print("=" * 60)

    metrics = {}

    for metric_id, config in MARKET_METRICS.items():

        result = fetch_metric(metric_id, config)

        metrics[metric_id] = result

        if result["status"] == "FRESH":

            print(
                f"✓ {metric_id:<8} "
                f"{result['value']} "
                f"{result['unit']} "
                f"({result['change_pct']}%)"
            )

        else:

            print(
                f"✗ {metric_id:<8} ERROR — "
                f"{result['error']}"
            )

    quality = calculate_quality(metrics)

    completed_at = datetime.now(timezone.utc)

    output = {
        "schema_version": "1.0",
        "generated_at": completed_at.isoformat(),
        "metrics": metrics,
        "data_quality": quality
    }

    with open(
        "live_market_data.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            output,
            file,
            ensure_ascii=False,
            indent=2
        )

    pipeline_status = {
        "pipeline": "P01-000B",
        "started_at": started_at.isoformat(),
        "completed_at": completed_at.isoformat(),
        "status": quality["status"],
        "data_quality": quality
    }

    with open(
        "pipeline_status.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            pipeline_status,
            file,
            ensure_ascii=False,
            indent=2
        )

    print("-" * 60)

    print(
        f"Fresh: {quality['fresh']} / "
        f"{quality['total']}"
    )

    print(
        f"Errors: {quality['error']}"
    )

    print(
        f"Data Quality: "
        f"{quality['score'] * 100:.0f}%"
    )

    print(
        f"Pipeline Status: "
        f"{quality['status']}"
    )

    print("=" * 60)

    # Important:
    # Do NOT fail the whole pipeline when one provider fails.
    # Individual source failures are recorded in JSON.
    #
    # But fail if absolutely no source works.
    if quality["fresh"] == 0:
        raise RuntimeError(
            "Pipeline failed: no market source returned valid data."
        )


if __name__ == "__main__":
    main()
