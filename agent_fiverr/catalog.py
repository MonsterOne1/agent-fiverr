"""Catalog loading and validation helpers."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Service:
    slug: str
    name: str
    category: str
    task_type: str
    archetype: str
    automation_level: str
    risk_level: str
    deliverable_types: tuple[str, ...]
    api_providers: tuple[str, ...]
    brief_fields: tuple[str, ...]
    output_fields: tuple[str, ...]
    qa_checks: tuple[str, ...]
    policy_rules: tuple[str, ...]
    golden_samples: tuple[str, ...]

    @classmethod
    def from_record(cls, record: dict[str, Any]) -> "Service":
        return cls(
            slug=record["slug"],
            name=record["name"],
            category=record["category"],
            task_type=record["task_type"],
            archetype=record["archetype"],
            automation_level=record["automation_level"],
            risk_level=record["risk_level"],
            deliverable_types=tuple(record["deliverable_types"]),
            api_providers=tuple(record["api_providers"]),
            brief_fields=tuple(record["brief_fields"]),
            output_fields=tuple(record["output_fields"]),
            qa_checks=tuple(record["qa_checks"]),
            policy_rules=tuple(record["policy_rules"]),
            golden_samples=tuple(record["golden_samples"]),
        )


class Catalog:
    def __init__(self, root: Path = ROOT):
        self.root = root
        self._services = self._load_services()
        self._providers = self._load_providers()

    @property
    def services(self) -> list[Service]:
        return list(self._services.values())

    @property
    def providers(self) -> dict[str, dict[str, Any]]:
        return dict(self._providers)

    def get_service(self, slug: str) -> Service:
        try:
            return self._services[slug]
        except KeyError as exc:
            raise KeyError(f"Unknown service slug: {slug}") from exc

    def validate_brief(self, service_slug: str, brief: dict[str, Any]) -> list[str]:
        service = self.get_service(service_slug)
        missing = [field for field in service.brief_fields if not brief.get(field)]
        return missing

    def provider_side_effect_levels(self, service_slug: str) -> dict[str, str]:
        service = self.get_service(service_slug)
        return {
            provider: self._providers[provider]["side_effect_level"]
            for provider in service.api_providers
        }

    def _load_services(self) -> dict[str, Service]:
        records = _load_json(self.root / "data" / "mvp-services.json")
        return {record["slug"]: Service.from_record(record) for record in records}

    def _load_providers(self) -> dict[str, dict[str, Any]]:
        matrix = _load_json(self.root / "data" / "api-provider-matrix.json")
        return {provider["id"]: provider for provider in matrix["providers"]}


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))

