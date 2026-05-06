#!/usr/bin/env python3
"""Run Marketplace Alpha metric thresholds against deterministic sample data."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from agent_fiverr.alpha_metrics import AlphaMetricGate, run_alpha_metrics_simulation


def main() -> int:
    report = run_alpha_metrics_simulation()
    result = AlphaMetricGate().evaluate(report)
    print("Alpha metrics simulation")
    print(f"Total orders: {report.total_orders}")
    print(f"Cancellation rate: {report.cancellation_rate:.1%}")
    print(f"Refund rate: {report.refund_rate:.1%}")
    print(f"Average first response: {report.average_first_response_seconds:.1f}s")
    print(f"Delivery speed improvement: {report.delivery_speed_improvement:.1%}")
    print(f"Gate: {'PASS' if result.passed else 'FAIL'}")
    for failure in result.failures:
        print(f"- {failure}")
    return 0 if result.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())

