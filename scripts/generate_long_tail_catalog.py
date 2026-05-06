#!/usr/bin/env python3
"""Generate Phase 4 long-tail service catalog draft."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from agent_fiverr.long_tail import generate_long_tail_services, validate_long_tail_services


def main() -> int:
    services = generate_long_tail_services(ROOT)
    result = validate_long_tail_services(services)
    output = ROOT / "data" / "long-tail-services.generated.json"
    output.write_text(json.dumps(services, indent=2) + "\n", encoding="utf-8")
    saleable = sum(1 for service in services if service["saleable_candidate"])
    print("Long-tail catalog generated.")
    print(f"Service specs: {len(services)}")
    print(f"Saleable candidates: {saleable}")
    print(f"Gate: {'PASS' if result.passed else 'FAIL'}")
    for failure in result.failures:
        print(f"- {failure}")
    return 0 if result.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())

