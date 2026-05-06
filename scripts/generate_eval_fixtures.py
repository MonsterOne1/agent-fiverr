#!/usr/bin/env python3
"""Generate the MVP eval fixture artifact."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from agent_fiverr.eval_fixtures import generate_eval_fixtures, validate_eval_fixtures


def main() -> int:
    fixtures = generate_eval_fixtures(ROOT)
    summary = validate_eval_fixtures(fixtures, ROOT)
    target = ROOT / "data" / "eval-fixtures.generated.json"
    target.write_text(json.dumps(fixtures, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("Eval fixtures generated.")
    print(f"Total fixtures: {summary.total_fixtures}")
    print(f"Services: {summary.services}")
    print(f"Fixtures per service: {summary.fixtures_per_service}")
    print("Gate: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
