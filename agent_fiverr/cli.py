"""Command line interface for local catalog and order runtime checks."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .catalog import Catalog
from .order import OrderRuntime


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(prog="agent-fiverr")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("list-services")

    brief_parser = sub.add_parser("validate-brief")
    brief_parser.add_argument("service_slug")
    brief_parser.add_argument("brief_json")

    create_parser = sub.add_parser("create-order")
    create_parser.add_argument("service_slug")
    create_parser.add_argument("brief_json")

    args = parser.parse_args()
    catalog = Catalog(ROOT)

    if args.command == "list-services":
        for service in catalog.services:
            print(f"{service.slug}\t{service.automation_level}\t{service.risk_level}\t{service.name}")
        return 0

    if args.command == "validate-brief":
        brief = _load_json_arg(args.brief_json)
        missing = catalog.validate_brief(args.service_slug, brief)
        print(json.dumps({"service": args.service_slug, "missing_fields": missing}, indent=2))
        return 1 if missing else 0

    if args.command == "create-order":
        brief = _load_json_arg(args.brief_json)
        runtime = OrderRuntime(ROOT, catalog)
        order = runtime.create_order(args.service_slug, brief)
        print(json.dumps({"order_id": order.order_id, "state": order.state, "missing_fields": order.missing_brief_fields}, indent=2))
        return 0

    return 2


def _load_json_arg(value: str):
    path = Path(value)
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return json.loads(value)


if __name__ == "__main__":
    raise SystemExit(main())

