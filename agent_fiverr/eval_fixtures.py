"""Generate executable eval fixtures for MVP service workspaces."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .catalog import Catalog
from .phase2_samples import generate_phase2_sample_orders


ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class EvalFixtureSummary:
    total_fixtures: int
    services: int
    fixtures_per_service: int


def generate_eval_fixtures(root: Path = ROOT, fixtures_per_service: int = 5) -> list[dict[str, Any]]:
    catalog = Catalog(root)
    samples = generate_phase2_sample_orders(root, samples_per_service=fixtures_per_service)
    fixtures: list[dict[str, Any]] = []
    for sample in samples:
        service = catalog.get_service(sample["service_slug"])
        fixture_id = sample["sample_id"].replace("-00", "-eval-00")
        fixtures.append(
            {
                "fixture_id": fixture_id,
                "service_slug": service.slug,
                "brief": sample["brief"],
                "expected_deliverable": {
                    field: f"Expected {field} for {fixture_id}"
                    for field in service.output_fields
                },
                "qa_expectations": list(service.qa_checks),
                "policy_expectations": list(service.policy_rules),
                "revision_scenario": {
                    "description": "Buyer asks for a wording or formatting change within the original brief.",
                    "changed_fields": [service.brief_fields[0]],
                    "expected_in_scope": True,
                },
                "minimum_pass": {
                    "brief_schema_valid": True,
                    "deliverable_schema_valid": True,
                    "qa_score_min": 4,
                    "unauthorized_side_effects": 0,
                },
            }
        )
    return fixtures


def validate_eval_fixtures(fixtures: list[dict[str, Any]], root: Path = ROOT, fixtures_per_service: int = 5) -> EvalFixtureSummary:
    catalog = Catalog(root)
    counts = {service.slug: 0 for service in catalog.services}
    fixture_ids: set[str] = set()
    for fixture in fixtures:
        fixture_id = fixture["fixture_id"]
        if fixture_id in fixture_ids:
            raise AssertionError(f"duplicate fixture id: {fixture_id}")
        fixture_ids.add(fixture_id)
        service = catalog.get_service(fixture["service_slug"])
        missing_brief = catalog.validate_brief(service.slug, fixture["brief"])
        if missing_brief:
            raise AssertionError(f"{fixture_id} missing brief fields: {missing_brief}")
        missing_output = [
            field
            for field in service.output_fields
            if not fixture["expected_deliverable"].get(field)
        ]
        if missing_output:
            raise AssertionError(f"{fixture_id} missing output fields: {missing_output}")
        if not fixture["qa_expectations"] or not fixture["policy_expectations"]:
            raise AssertionError(f"{fixture_id} missing QA or policy expectations")
        if fixture["minimum_pass"]["qa_score_min"] < 4:
            raise AssertionError(f"{fixture_id} minimum QA score is below delivery threshold")
        counts[service.slug] += 1

    for service_slug, count in counts.items():
        if count != fixtures_per_service:
            raise AssertionError(f"{service_slug} expected {fixtures_per_service} fixtures, found {count}")

    return EvalFixtureSummary(
        total_fixtures=len(fixtures),
        services=len(counts),
        fixtures_per_service=fixtures_per_service,
    )
