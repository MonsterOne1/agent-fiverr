"""Phase 4 long-tail service catalog generation."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .catalog import Catalog


ROOT = Path(__file__).resolve().parents[1]
TASK_VARIANTS = [
    "audit",
    "draft",
    "cleanup",
    "setup",
    "optimization",
    "strategy",
    "localization",
    "automation",
    "repurpose",
    "qa",
    "report",
    "template",
    "research",
    "conversion",
    "asset",
    "workflow",
    "migration",
    "integration",
    "monitoring",
    "training",
    "launch",
    "maintenance",
    "analysis",
    "planner",
    "formatter",
    "generator",
    "review",
    "brief",
    "playbook",
    "dashboard",
    "sequence",
    "assistant",
    "validator",
    "enrichment",
    "summary",
    "transformation",
    "extractor",
    "composer",
    "editor",
    "concierge",
]


@dataclass(frozen=True)
class LongTailValidationResult:
    passed: bool
    failures: tuple[str, ...]


def generate_long_tail_services(root: Path = ROOT) -> list[dict[str, Any]]:
    catalog = Catalog(root)
    services: list[dict[str, Any]] = []
    for base in catalog.services:
        for variant_index, variant in enumerate(TASK_VARIANTS, start=1):
            slug = f"{base.slug}-{variant}"
            saleable = base.automation_level in {"L3", "L4", "L5"} and variant_index <= 8
            services.append(
                {
                    "slug": slug,
                    "base_service": base.slug,
                    "name": f"{base.name} {variant.title()}",
                    "category": base.category,
                    "task_type": f"{base.task_type}_{variant}",
                    "automation_level": base.automation_level,
                    "risk_level": base.risk_level,
                    "saleable_candidate": saleable,
                    "minimum_eval_pack": {
                        "brief": f"{slug}/brief.json",
                        "expected_outline": f"{slug}/expected_outline.md",
                        "qa_checklist": f"{slug}/qa_checklist.json",
                        "policy_expectations": f"{slug}/policy_expectations.json",
                    },
                }
            )
    return services


def validate_long_tail_services(services: list[dict[str, Any]]) -> LongTailValidationResult:
    failures: list[str] = []
    slugs = [service.get("slug") for service in services]
    if len(services) < 500:
        failures.append("long-tail catalog has fewer than 500 service specs")
    if len(slugs) != len(set(slugs)):
        failures.append("long-tail catalog has duplicate slugs")
    saleable_count = sum(1 for service in services if service.get("saleable_candidate"))
    if saleable_count < 100:
        failures.append("long-tail catalog has fewer than 100 saleable candidates")
    for service in services:
        eval_pack = service.get("minimum_eval_pack", {})
        required = {"brief", "expected_outline", "qa_checklist", "policy_expectations"}
        if set(eval_pack) != required:
            failures.append(f"{service.get('slug')} missing minimum eval pack")
            break
    return LongTailValidationResult(passed=not failures, failures=tuple(failures))

