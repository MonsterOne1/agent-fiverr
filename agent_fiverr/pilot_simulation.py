"""Pilot sample order simulation."""

from __future__ import annotations

import json
import tempfile
from dataclasses import dataclass
from pathlib import Path

from .catalog import Catalog
from .order import OrderRuntime


ROOT = Path(__file__).resolve().parents[1]
PILOT_SAMPLE_PATH = ROOT / "data" / "pilot-sample-orders.json"


@dataclass(frozen=True)
class SimulationSummary:
    total_orders: int
    delivered_orders: int
    services: tuple[str, ...]


def run_pilot_simulation(root: Path = ROOT) -> SimulationSummary:
    samples = json.loads((root / "data" / "pilot-sample-orders.json").read_text(encoding="utf-8"))
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
            payload = {
                field: f"Simulated {field} for {sample['sample_id']}"
                for field in service.output_fields
            }
            runtime.add_deliverable(order, payload, qa_score=4, qa_notes=sample["qa_expectations"])
            runtime.transition(order, "delivery")
            delivered += 1
            services.add(service.slug)

    return SimulationSummary(
        total_orders=len(samples),
        delivered_orders=delivered,
        services=tuple(sorted(services)),
    )

