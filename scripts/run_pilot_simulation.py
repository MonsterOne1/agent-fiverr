#!/usr/bin/env python3
"""Run 30 seed pilot orders through the local lifecycle runtime."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from agent_fiverr.pilot_simulation import run_pilot_simulation


def main() -> int:
    summary = run_pilot_simulation()
    print(
        "Pilot simulation passed.\n"
        f"Total orders: {summary.total_orders}\n"
        f"Delivered orders: {summary.delivered_orders}\n"
        f"Services: {', '.join(summary.services)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
