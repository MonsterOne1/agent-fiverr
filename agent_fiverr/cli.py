"""Command line interface for local catalog and order runtime checks."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from .catalog import Catalog
from .marketplace import Marketplace
from .order import OrderRuntime


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(prog="agent-fiverr")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("list-services")

    discover_parser = sub.add_parser("discover")
    discover_parser.add_argument("--category")
    discover_parser.add_argument("--task-type")

    brief_parser = sub.add_parser("validate-brief")
    brief_parser.add_argument("service_slug")
    brief_parser.add_argument("brief_json")

    create_parser = sub.add_parser("create-order")
    create_parser.add_argument("service_slug")
    create_parser.add_argument("brief_json")

    quote_parser = sub.add_parser("quote")
    quote_parser.add_argument("service_slug")
    quote_parser.add_argument("brief_json")
    quote_parser.add_argument("--package", choices=["basic", "standard", "premium"], default="basic")

    accept_parser = sub.add_parser("accept-quote")
    accept_parser.add_argument("service_slug")
    accept_parser.add_argument("brief_json")
    accept_parser.add_argument("--package", choices=["basic", "standard", "premium"], default="basic")
    accept_parser.add_argument("--buyer-id", required=True)
    accept_parser.add_argument("--escrow-provider", choices=["mock", "stripe_connect"], default="mock")

    args = parser.parse_args()
    catalog = Catalog(ROOT)

    if args.command == "list-services":
        for service in catalog.services:
            print(f"{service.slug}\t{service.automation_level}\t{service.risk_level}\t{service.name}")
        return 0

    if args.command == "discover":
        marketplace = Marketplace(catalog, OrderRuntime(ROOT, catalog))
        for service in marketplace.discover(category=args.category, task_type=args.task_type):
            print(f"{service.slug}\t{service.category}\t{service.task_type}\t{service.name}")
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

    if args.command == "quote":
        brief = _load_json_arg(args.brief_json)
        marketplace = Marketplace(catalog, OrderRuntime(ROOT, catalog))
        quote = marketplace.quote(args.service_slug, brief, package=args.package)
        print(json.dumps(asdict(quote), indent=2))
        return 0 if quote.ready else 1

    if args.command == "accept-quote":
        brief = _load_json_arg(args.brief_json)
        marketplace = Marketplace(catalog, OrderRuntime(ROOT, catalog))
        quote = marketplace.quote(args.service_slug, brief, package=args.package)
        checkout = marketplace.accept_quote(quote, buyer_id=args.buyer_id, escrow_provider=args.escrow_provider)
        print(json.dumps(asdict(checkout), indent=2))
        return 0

    return 2


def _load_json_arg(value: str):
    path = Path(value)
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return json.loads(value)


if __name__ == "__main__":
    raise SystemExit(main())
