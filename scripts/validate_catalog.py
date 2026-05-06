#!/usr/bin/env python3
"""Validate Phase 0/1 Agent Fiverr catalog artifacts without external deps."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from agent_fiverr.providers import adapter_for

REQUIRED_SERVICE_FILES = {
    "SERVICE.md",
    "BRIEF_SCHEMA.json",
    "DELIVERABLE_SCHEMA.json",
    "QUOTE_RULES.md",
    "QA_RUBRIC.md",
    "EVALS.md",
    "TOOLS.md",
    "POLICY.md",
    "REVISION.md",
    "HANDOFF.md",
    "WORKSPACE_MANIFEST.json",
}
REQUIRED_LIFECYCLE = [
    "intake",
    "scope_check",
    "quote",
    "plan",
    "work",
    "qa",
    "delivery",
    "revision",
    "close",
    "memory",
]
SIDE_EFFECT_PROVIDER_LEVELS = {
    "requires_explicit_authorization",
}
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise AssertionError(f"{path.relative_to(ROOT)} is invalid JSON: {exc}") from exc


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def validate_service_record(service: dict, categories: set[str], archetypes: set[str], providers: set[str]) -> None:
    required = [
        "slug",
        "name",
        "category",
        "task_type",
        "archetype",
        "automation_level",
        "risk_level",
        "deliverable_types",
        "api_providers",
        "brief_fields",
        "output_fields",
        "qa_checks",
        "policy_rules",
        "golden_samples",
    ]
    for field in required:
        assert_true(field in service, f"{service.get('slug', '<unknown>')} missing {field}")
    assert_true(bool(SLUG_RE.match(service["slug"])), f"invalid slug: {service['slug']}")
    assert_true(service["category"] in categories, f"{service['slug']} has unknown category {service['category']}")
    assert_true(service["archetype"] in archetypes, f"{service['slug']} has unknown archetype {service['archetype']}")
    assert_true(service["automation_level"] in {"L1", "L2", "L3", "L4", "L5"}, f"{service['slug']} has invalid automation level")
    assert_true(service["risk_level"] in {"low", "medium", "high"}, f"{service['slug']} has invalid risk level")
    for list_field, min_len in {
        "deliverable_types": 1,
        "api_providers": 1,
        "brief_fields": 3,
        "output_fields": 3,
        "qa_checks": 2,
        "policy_rules": 1,
        "golden_samples": 1,
    }.items():
        value = service[list_field]
        assert_true(isinstance(value, list) and len(value) >= min_len, f"{service['slug']} has too few {list_field}")
        assert_true(all(isinstance(item, str) and item for item in value), f"{service['slug']} has invalid {list_field}")
    unknown_providers = sorted(set(service["api_providers"]) - providers)
    assert_true(not unknown_providers, f"{service['slug']} uses unknown providers: {unknown_providers}")


def validate_generated_workspace(service: dict, provider_levels: dict[str, str]) -> None:
    service_dir = ROOT / "services" / service["slug"]
    assert_true(service_dir.is_dir(), f"missing generated workspace for {service['slug']}")
    files = {path.name for path in service_dir.iterdir() if path.is_file()}
    missing = sorted(REQUIRED_SERVICE_FILES - files)
    assert_true(not missing, f"{service['slug']} missing files: {missing}")

    brief = load_json(service_dir / "BRIEF_SCHEMA.json")
    deliverable = load_json(service_dir / "DELIVERABLE_SCHEMA.json")
    manifest = load_json(service_dir / "WORKSPACE_MANIFEST.json")

    assert_true(set(service["brief_fields"]).issubset(set(brief["required"])), f"{service['slug']} brief schema missing required fields")
    assert_true(set(service["output_fields"]).issubset(set(deliverable["required"])), f"{service['slug']} deliverable schema missing required fields")
    assert_true(manifest["required_files"] == sorted(REQUIRED_SERVICE_FILES) or set(manifest["required_files"]) == REQUIRED_SERVICE_FILES, f"{service['slug']} manifest file list mismatch")
    assert_true(manifest["lifecycle"] == REQUIRED_LIFECYCLE, f"{service['slug']} lifecycle mismatch")
    assert_true(set(service["qa_checks"]).issubset(set(manifest["quality_gates"])), f"{service['slug']} manifest missing QA checks")

    needs_auth = any(provider_levels[provider] in SIDE_EFFECT_PROVIDER_LEVELS for provider in service["api_providers"])
    if needs_auth:
        policy_text = (service_dir / "POLICY.md").read_text(encoding="utf-8")
        assert_true("explicit authorization" in policy_text, f"{service['slug']} missing explicit authorization policy")


def validate_template() -> None:
    template_dir = ROOT / "templates" / "agent-service-template"
    assert_true(template_dir.is_dir(), "missing agent-service-template directory")
    files = {path.name for path in template_dir.iterdir() if path.is_file()}
    missing = sorted(REQUIRED_SERVICE_FILES - files)
    assert_true(not missing, f"template missing files: {missing}")
    manifest = load_json(template_dir / "WORKSPACE_MANIFEST.json")
    assert_true(manifest["lifecycle"] == REQUIRED_LIFECYCLE, "template lifecycle mismatch")


def validate_provider_adapters(provider_records: list[dict]) -> None:
    for provider in provider_records:
        adapter = adapter_for(provider["id"])
        assert_true(adapter.provider_id == provider["id"], f"{provider['id']} adapter id mismatch")
        assert_true(bool(adapter.actions), f"{provider['id']} adapter has no actions")
        assert_true(bool(adapter.scopes), f"{provider['id']} adapter has no scopes")
        assert_true(bool(adapter.artifact_types), f"{provider['id']} adapter has no artifact types")


def validate_pilot_samples(services: list[dict]) -> None:
    samples = load_json(ROOT / "data" / "pilot-sample-orders.json")
    service_slugs = {service["slug"] for service in services}
    pilot_slugs = {"seo-geo-audit", "data-cleaning-formatting", "presentation-pitch-deck"}
    counts = {slug: 0 for slug in pilot_slugs}
    seen_sample_ids: set[str] = set()
    for sample in samples:
        for field in [
            "service_slug",
            "sample_id",
            "brief",
            "expected_deliverables",
            "qa_expectations",
            "policy_expectations",
        ]:
            assert_true(field in sample, f"pilot sample missing {field}: {sample}")
        assert_true(sample["service_slug"] in service_slugs, f"unknown pilot sample service {sample['service_slug']}")
        assert_true(sample["service_slug"] in pilot_slugs, f"sample belongs to non-pilot service {sample['service_slug']}")
        assert_true(sample["sample_id"] not in seen_sample_ids, f"duplicate sample id {sample['sample_id']}")
        seen_sample_ids.add(sample["sample_id"])
        assert_true(isinstance(sample["brief"], dict) and sample["brief"], f"{sample['sample_id']} has empty brief")
        for list_field in ["expected_deliverables", "qa_expectations", "policy_expectations"]:
            assert_true(
                isinstance(sample[list_field], list) and sample[list_field],
                f"{sample['sample_id']} has empty {list_field}",
            )
        counts[sample["service_slug"]] += 1
    assert_true(len(samples) == 30, f"expected 30 pilot samples, found {len(samples)}")
    for slug, count in counts.items():
        assert_true(count == 10, f"expected 10 samples for {slug}, found {count}")


def main() -> int:
    categories = {item["category"] for item in load_json(ROOT / "data" / "top-level-categories.json")}
    archetypes = {item["id"] for item in load_json(ROOT / "data" / "service-archetypes.json")}
    provider_records = load_json(ROOT / "data" / "api-provider-matrix.json")["providers"]
    providers = {item["id"] for item in provider_records}
    provider_levels = {item["id"]: item["side_effect_level"] for item in provider_records}
    services = load_json(ROOT / "data" / "mvp-services.json")

    errors: list[str] = []
    try:
        assert_true(len(categories) >= 14, "top-level category coverage below plan baseline")
        assert_true(len(services) == 20, f"expected 20 MVP services, found {len(services)}")
        slugs = [service["slug"] for service in services]
        assert_true(len(slugs) == len(set(slugs)), "duplicate service slugs")
        for service in services:
            validate_service_record(service, categories, archetypes, providers)
            validate_generated_workspace(service, provider_levels)
        validate_template()
        validate_provider_adapters(provider_records)
        validate_pilot_samples(services)
    except AssertionError as exc:
        errors.append(str(exc))

    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1

    print("Catalog validation passed.")
    print(f"Top-level categories: {len(categories)}")
    print(f"MVP services: {len(services)}")
    print(f"Providers: {len(providers)}")
    print(f"Provider adapters: {len(providers)}")
    print("Pilot sample orders: 30")
    print(f"Required files per service: {len(REQUIRED_SERVICE_FILES)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
