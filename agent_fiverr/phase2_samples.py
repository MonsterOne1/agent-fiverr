"""Generate and simulate Phase 2 MVP sample orders."""

from __future__ import annotations

import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .catalog import Catalog, Service
from .order import OrderRuntime


ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Phase2SimulationSummary:
    total_orders: int
    delivered_orders: int
    services: tuple[str, ...]


def generate_phase2_sample_orders(root: Path = ROOT, samples_per_service: int = 10) -> list[dict[str, Any]]:
    catalog = Catalog(root)
    samples: list[dict[str, Any]] = []
    for service in sorted(catalog.services, key=lambda item: item.slug):
        for index in range(1, samples_per_service + 1):
            samples.append(_sample_for_service(service, index))
    return samples


def run_phase2_simulation(root: Path = ROOT) -> Phase2SimulationSummary:
    samples = generate_phase2_sample_orders(root)
    with tempfile.TemporaryDirectory() as tmp_dir:
        runtime_root = Path(tmp_dir)
        for dirname in ["data", "services"]:
            (runtime_root / dirname).symlink_to(root / dirname, target_is_directory=True)
        catalog = Catalog(runtime_root)
        runtime = OrderRuntime(runtime_root, catalog)

        delivered = 0
        services: set[str] = set()
        for sample in samples:
            service = catalog.get_service(sample["service_slug"])
            order = runtime.create_order(service.slug, sample["brief"])
            if order.missing_brief_fields:
                raise AssertionError(f"{sample['sample_id']} missing brief fields: {order.missing_brief_fields}")
            for state in ["scope_check", "quote", "plan", "work", "qa"]:
                runtime.transition(order, state)  # type: ignore[arg-type]
            runtime.add_deliverable(
                order,
                {
                    field: f"Simulated {field} for {sample['sample_id']}"
                    for field in service.output_fields
                },
                qa_score=4,
                qa_notes=sample["qa_expectations"],
            )
            runtime.transition(order, "delivery")
            delivered += 1
            services.add(service.slug)

    return Phase2SimulationSummary(
        total_orders=len(samples),
        delivered_orders=delivered,
        services=tuple(sorted(services)),
    )


def _sample_for_service(service: Service, index: int) -> dict[str, Any]:
    sample_id = f"{service.slug}-{index:03d}"
    return {
        "service_slug": service.slug,
        "sample_id": sample_id,
        "brief": {
            field: _brief_value(service, field, index)
            for field in service.brief_fields
        },
        "expected_deliverables": list(service.deliverable_types),
        "qa_expectations": list(service.qa_checks),
        "policy_expectations": list(service.policy_rules),
    }


def _brief_value(service: Service, field: str, index: int) -> str:
    readable = field.replace("_", " ")
    return f"{service.name} sample {index} {readable}"

