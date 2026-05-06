"""Simulated cost gate for MVP service economics."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .catalog import Catalog, Service
from .marketplace import LEVEL_MULTIPLIER, PACKAGE_RULES, Package


ROOT = Path(__file__).resolve().parents[1]


PROVIDER_COST_USD = {
    "openai_responses": 2.00,
    "gpt_image_2": 4.00,
    "banana": 4.00,
    "seedance": 8.00,
    "kling": 8.00,
    "renoise": 6.00,
    "suno": 3.00,
    "elevenlabs": 3.00,
    "browser_search": 1.00,
    "github": 1.50,
    "vercel": 1.50,
    "wordpress": 1.50,
    "shopify": 1.50,
    "google_ads": 1.00,
}

PACKAGE_COST_MULTIPLIER: dict[Package, float] = {
    "basic": 0.75,
    "standard": 1.00,
    "premium": 1.60,
}

AUTOMATION_OVERHEAD_USD = {
    "L1": 25.00,
    "L2": 20.00,
    "L3": 10.00,
    "L4": 7.50,
    "L5": 4.00,
}


@dataclass(frozen=True)
class ServiceCostEstimate:
    service_slug: str
    package: Package
    price_usd: int
    estimated_cost_usd: float
    cost_ratio: float
    gate_pass: bool


@dataclass(frozen=True)
class CostGateSummary:
    services_checked: int
    package: Package
    threshold: float
    max_cost_ratio: float
    failing_services: tuple[str, ...]

    @property
    def gate_pass(self) -> bool:
        return not self.failing_services


def estimate_service_cost(service: Service, package: Package = "standard", threshold: float = 0.30) -> ServiceCostEstimate:
    price = int(PACKAGE_RULES[package][0] * LEVEL_MULTIPLIER[service.automation_level])
    provider_cost = sum(PROVIDER_COST_USD[provider] for provider in service.api_providers)
    overhead = AUTOMATION_OVERHEAD_USD[service.automation_level]
    estimated_cost = round((provider_cost + overhead) * PACKAGE_COST_MULTIPLIER[package], 2)
    ratio = round(estimated_cost / price, 4)
    return ServiceCostEstimate(
        service_slug=service.slug,
        package=package,
        price_usd=price,
        estimated_cost_usd=estimated_cost,
        cost_ratio=ratio,
        gate_pass=ratio <= threshold,
    )


def run_cost_gate(root: Path = ROOT, package: Package = "standard", threshold: float = 0.30) -> tuple[CostGateSummary, list[ServiceCostEstimate]]:
    catalog = Catalog(root)
    estimates = [estimate_service_cost(service, package=package, threshold=threshold) for service in catalog.services]
    failing = tuple(sorted(estimate.service_slug for estimate in estimates if not estimate.gate_pass))
    summary = CostGateSummary(
        services_checked=len(estimates),
        package=package,
        threshold=threshold,
        max_cost_ratio=max(estimate.cost_ratio for estimate in estimates),
        failing_services=failing,
    )
    return summary, estimates
