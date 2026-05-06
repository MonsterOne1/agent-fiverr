"""Generate and simulate Phase 2 MVP sample orders."""

from __future__ import annotations

import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .catalog import Catalog, Service
from .order import OrderRuntime
from .providers import ProviderRuntime
from .qa import HumanReviewQueue, QAEvaluator


ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Phase2SimulationSummary:
    total_orders: int
    delivered_orders: int
    services: tuple[str, ...]
    provider_traces: int
    qa_evaluations: int
    human_review_items: int


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
        providers = ProviderRuntime(catalog)
        evaluator = QAEvaluator(catalog)
        review_queue = HumanReviewQueue()

        delivered = 0
        provider_traces = 0
        qa_evaluations = 0
        services: set[str] = set()
        for sample in samples:
            service = catalog.get_service(sample["service_slug"])
            order = runtime.create_order(service.slug, sample["brief"])
            if order.missing_brief_fields:
                raise AssertionError(f"{sample['sample_id']} missing brief fields: {order.missing_brief_fields}")
            for state in ["scope_check", "quote", "plan", "work", "qa"]:
                runtime.transition(order, state)  # type: ignore[arg-type]
            payload = {
                field: f"Simulated {field} for {sample['sample_id']}"
                for field in service.output_fields
            }
            rubric_evidence = {
                check: f"Evidence for {check} in {sample['sample_id']}"
                for check in service.qa_checks
            }
            qa_result = evaluator.evaluate(service.slug, payload, rubric_evidence=rubric_evidence)
            qa_evaluations += 1
            if qa_result.status == "block":
                raise AssertionError(f"{sample['sample_id']} blocked by QA: {qa_result.reasons}")
            if qa_result.status == "human_review":
                review_queue.enqueue(order.order_id, service.slug, qa_result)
            runtime.add_deliverable(order, payload, qa_score=qa_result.score, qa_notes=list(qa_result.reasons))
            for provider_id in service.api_providers:
                providers.run(
                    service.slug,
                    provider_id,
                    "simulate_provider_output",
                    {"sample_id": sample["sample_id"]},
                    dry_run=True,
                )
                provider_traces += 1
            runtime.transition(order, "delivery")
            delivered += 1
            services.add(service.slug)

    return Phase2SimulationSummary(
        total_orders=len(samples),
        delivered_orders=delivered,
        services=tuple(sorted(services)),
        provider_traces=provider_traces,
        qa_evaluations=qa_evaluations,
        human_review_items=len(review_queue.items),
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
