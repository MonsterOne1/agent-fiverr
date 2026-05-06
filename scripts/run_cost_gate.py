#!/usr/bin/env python3
"""Run the local MVP service cost gate."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from agent_fiverr.costs import run_cost_gate


def main() -> int:
    summary, _ = run_cost_gate(ROOT)
    print("Cost gate simulation")
    print(f"Services checked: {summary.services_checked}")
    print(f"Package: {summary.package}")
    print(f"Threshold: {summary.threshold:.0%}")
    print(f"Max cost ratio: {summary.max_cost_ratio:.1%}")
    print(f"Gate: {'PASS' if summary.gate_pass else 'FAIL'}")
    if not summary.gate_pass:
        print(f"Failing services: {', '.join(summary.failing_services)}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
