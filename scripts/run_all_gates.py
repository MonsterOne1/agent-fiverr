#!/usr/bin/env python3
"""Run all local Agent Fiverr acceptance gates."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

GATE_COMMANDS: tuple[tuple[str, ...], ...] = (
    ("python3", "scripts/validate_catalog.py"),
    ("python3", "scripts/run_pilot_simulation.py"),
    ("python3", "scripts/run_phase2_simulation.py"),
    ("python3", "scripts/run_alpha_metrics.py"),
    ("python3", "scripts/run_cost_gate.py"),
    ("python3", "scripts/generate_long_tail_catalog.py"),
    ("python3", "scripts/generate_eval_fixtures.py"),
    ("python3", "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"),
    ("git", "diff", "--check"),
)


def main() -> int:
    for command in GATE_COMMANDS:
        print(f"$ {' '.join(command)}")
        result = subprocess.run(command, cwd=ROOT, text=True, check=False)
        if result.returncode != 0:
            print(f"Gate failed: {' '.join(command)}", file=sys.stderr)
            return result.returncode
    print("All local gates passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
