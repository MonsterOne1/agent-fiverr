"""Local marketplace orchestrator for service discovery, quotes, and escrow mock."""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from typing import Literal

from .catalog import Catalog, Service
from .order import OrderRuntime


Package = Literal["basic", "standard", "premium"]

PACKAGE_RULES: dict[Package, tuple[int, int]] = {
    "basic": (75, 48),
    "standard": (150, 24),
    "premium": (300, 12),
}

LEVEL_MULTIPLIER = {
    "L1": 1.2,
    "L2": 2.0,
    "L3": 1.5,
    "L4": 1.25,
    "L5": 1.0,
}


@dataclass(frozen=True)
class Quote:
    quote_id: str
    service_slug: str
    package: Package
    ready: bool
    price_usd: int
    sla_hours: int
    missing_fields: tuple[str, ...]
    assumptions: tuple[str, ...]
    brief: dict[str, object]


@dataclass(frozen=True)
class Checkout:
    checkout_id: str
    order_id: str
    quote_id: str
    buyer_id: str
    amount_usd: int
    escrow_status: str


class Marketplace:
    def __init__(self, catalog: Catalog, order_runtime: OrderRuntime):
        self.catalog = catalog
        self.order_runtime = order_runtime

    def discover(self, *, category: str | None = None, task_type: str | None = None) -> list[Service]:
        services = self.catalog.services
        if category is not None:
            services = [service for service in services if service.category == category]
        if task_type is not None:
            services = [service for service in services if service.task_type == task_type]
        return sorted(services, key=lambda service: service.slug)

    def quote(self, service_slug: str, brief: dict[str, object], package: Package = "basic") -> Quote:
        service = self.catalog.get_service(service_slug)
        missing = tuple(self.catalog.validate_brief(service_slug, brief))
        base_price, sla_hours = PACKAGE_RULES[package]
        price = int(base_price * LEVEL_MULTIPLIER[service.automation_level])
        assumptions = tuple(f"Assumes buyer input for {field} remains stable." for field in service.brief_fields[:2])
        return Quote(
            quote_id=str(uuid.uuid4()),
            service_slug=service_slug,
            package=package,
            ready=not missing,
            price_usd=price,
            sla_hours=sla_hours,
            missing_fields=missing,
            assumptions=assumptions,
            brief=brief,
        )

    def accept_quote(self, quote: Quote, buyer_id: str) -> Checkout:
        if not quote.ready:
            raise ValueError("Cannot accept quote with missing brief fields.")
        order = self.order_runtime.create_order(quote.service_slug, quote.brief)
        return Checkout(
            checkout_id=str(uuid.uuid4()),
            order_id=order.order_id,
            quote_id=quote.quote_id,
            buyer_id=buyer_id,
            amount_usd=quote.price_usd,
            escrow_status="held",
        )

