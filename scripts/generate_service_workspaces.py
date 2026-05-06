#!/usr/bin/env python3
"""Generate service workspace spec folders from data/mvp-services.json."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "mvp-services.json"
SERVICES_DIR = ROOT / "services"
TEMPLATE_DIR = ROOT / "templates" / "agent-service-template"

LIFECYCLE = [
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

REQUIRED_FILES = [
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
]


def title_from_key(key: str) -> str:
    return key.replace("_", " ").replace("-", " ").title()


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def schema_from_fields(title: str, fields: list[str]) -> dict:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": title,
        "type": "object",
        "required": fields,
        "properties": {
            field: {
                "type": "string",
                "title": title_from_key(field),
                "minLength": 1,
            }
            for field in fields
        },
        "additionalProperties": True,
    }


def markdown_list(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def service_markdown(service: dict) -> str:
    return f"""# {service["name"]}

## Positioning

Category: {service["category"]}
Task type: `{service["task_type"]}`
Archetype: `{service["archetype"]}`
Automation level: `{service["automation_level"]}`
Risk level: `{service["risk_level"]}`

## Scope

This agent handles intake, scope validation, quoting, planning, production, QA,
delivery, revision handling, and memory capture for this service.

## Deliverables

{markdown_list(service["deliverable_types"])}

## Required Buyer Inputs

{markdown_list(service["brief_fields"])}

## Completion Standard

The order can be delivered only when every QA check in `QA_RUBRIC.md` is passed
or explicitly escalated according to `POLICY.md`.
"""


def quote_rules(service: dict) -> str:
    return f"""# Quote Rules

## Packages

- Basic: narrow single-output delivery with one revision.
- Standard: complete delivery with two revisions and source files when applicable.
- Premium: complete delivery, variants, QA notes, and priority turnaround.

## Pricing Variables

- Input complexity and missing brief fields.
- Number and type of deliverables: {", ".join(service["deliverable_types"])}.
- Required provider APIs: {", ".join(service["api_providers"])}.
- Automation level: {service["automation_level"]}.
- Risk level: {service["risk_level"]}.

## Requote Triggers

- Buyer changes the target audience, platform, product, source data, or delivery
  format after work starts.
- Buyer asks for external side effects not included in the original scope.
- Policy escalation requires human expert review.
"""


def qa_rubric(service: dict) -> str:
    return f"""# QA Rubric

## Required Checks

{markdown_list(service["qa_checks"])}

## Universal Checks

- Brief is complete or missing fields are listed as assumptions.
- Deliverable matches `DELIVERABLE_SCHEMA.json`.
- Provider/API outputs are logged in `TOOLS.md` or the order trace.
- High-risk claims and side effects are escalated before delivery.

## Scoring

- 5: Ready to deliver with no material issues.
- 4: Ready with minor notes.
- 3: Needs revision before delivery.
- 2: Requires human review.
- 1: Out of scope or unsafe.

Delivery threshold: 4 or higher.
"""


def policy(service: dict) -> str:
    return f"""# Policy

Risk level: `{service["risk_level"]}`

## Service-Specific Rules

{markdown_list(service["policy_rules"])}

## Authorization Gates

- External publishing, account mutation, ad spend, production deploys, payment
  actions, and email/social sends require explicit authorization from the buyer.
- Provider API keys are supplied by the owner later and must never be committed.
- Generated media must include provider/source notes in the asset manifest.

## Escalation

Escalate to human review when the task involves regulated advice, irreversible
account changes, unclear IP rights, safety-sensitive claims, or unresolved buyer
approval.
"""


def tools(service: dict) -> str:
    return f"""# Tools

## Required Providers

{markdown_list(service["api_providers"])}

## Credential Handling

Provider IDs are committed here; keys are not. Expected key delivery options:

- `.env` for local development.
- Secret manager for hosted workspaces.
- Per-workspace provider authorization for buyer-owned accounts.

## Side-Effect Discipline

Read-only analysis may run automatically. Account changes, deployments,
publishing, payments, ad spend, and outbound communication require explicit
authorization in the order trace.
"""


def evals(service: dict) -> str:
    return f"""# Evals

## Golden Samples

{markdown_list(service["golden_samples"])}

## Minimum Eval Pack

Each golden sample must include:

- `brief.json`
- expected deliverable outline
- QA checklist result
- policy escalation expectations
- revision scenario

## Pass Criteria

- Brief schema validates.
- Deliverable schema validates.
- QA score is 4 or higher.
- No unauthorized side effects.
"""


def revision() -> str:
    return """# Revision Policy

## Included Revisions

Revisions are included when the buyer asks for changes within the original
brief, target audience, deliverable type, and platform.

## Scope Changes

Requote when the buyer changes the core goal, adds new platforms, requires a
new data source, requests new provider output, or asks for production actions
not included in the approved quote.
"""


def handoff() -> str:
    return """# Handoff

## Human Expert Handoff

Use when regulated, brand-critical, safety-sensitive, or high-liability review
is needed.

## Agent Handoff

Use when another specialist agent owns a required capability. Handoffs must
include the brief, current status, open risks, expected output, and completion
marker.
"""


def manifest(service: dict) -> dict:
    auth_gates = [
        "external_publishing",
        "account_mutation",
        "ad_spend",
        "production_deploy",
        "payment_action",
        "outbound_message_send",
    ]
    return {
        "service": service["slug"],
        "required_files": REQUIRED_FILES,
        "lifecycle": LIFECYCLE,
        "quality_gates": service["qa_checks"],
        "authorization_gates": auth_gates,
    }


def generate_service(service: dict) -> None:
    target = SERVICES_DIR / service["slug"]
    write(target / "SERVICE.md", service_markdown(service))
    write(
        target / "BRIEF_SCHEMA.json",
        json.dumps(schema_from_fields(f'{service["name"]} Brief', service["brief_fields"]), indent=2)
        + "\n",
    )
    write(
        target / "DELIVERABLE_SCHEMA.json",
        json.dumps(schema_from_fields(f'{service["name"]} Deliverable', service["output_fields"]), indent=2)
        + "\n",
    )
    write(target / "QUOTE_RULES.md", quote_rules(service))
    write(target / "QA_RUBRIC.md", qa_rubric(service))
    write(target / "EVALS.md", evals(service))
    write(target / "TOOLS.md", tools(service))
    write(target / "POLICY.md", policy(service))
    write(target / "REVISION.md", revision())
    write(target / "HANDOFF.md", handoff())
    write(target / "WORKSPACE_MANIFEST.json", json.dumps(manifest(service), indent=2) + "\n")


def generate_template() -> None:
    write(
        TEMPLATE_DIR / "SERVICE.md",
        "# {{SERVICE_NAME}}\n\nDefine scope, non-scope, buyer profile, deliverables, and completion standard.\n",
    )
    write(
        TEMPLATE_DIR / "BRIEF_SCHEMA.json",
        json.dumps(schema_from_fields("{{SERVICE_NAME}} Brief", ["buyer_goal", "target_audience", "constraints"]), indent=2)
        + "\n",
    )
    write(
        TEMPLATE_DIR / "DELIVERABLE_SCHEMA.json",
        json.dumps(schema_from_fields("{{SERVICE_NAME}} Deliverable", ["summary", "deliverables", "qa_notes"]), indent=2)
        + "\n",
    )
    for file_name, heading in [
        ("QUOTE_RULES.md", "Quote Rules"),
        ("QA_RUBRIC.md", "QA Rubric"),
        ("EVALS.md", "Evals"),
        ("TOOLS.md", "Tools"),
        ("POLICY.md", "Policy"),
        ("REVISION.md", "Revision Policy"),
        ("HANDOFF.md", "Handoff"),
    ]:
        write(TEMPLATE_DIR / file_name, f"# {heading}\n\nReplace placeholders for this service.\n")
    write(
        TEMPLATE_DIR / "WORKSPACE_MANIFEST.json",
        json.dumps(
            {
                "service": "{{SERVICE_SLUG}}",
                "required_files": REQUIRED_FILES,
                "lifecycle": LIFECYCLE,
                "quality_gates": ["brief_complete", "deliverable_schema_valid", "policy_checked"],
                "authorization_gates": ["external_side_effects"],
            },
            indent=2,
        )
        + "\n",
    )


def main() -> None:
    services = json.loads(DATA.read_text(encoding="utf-8"))
    for service in services:
        generate_service(service)
    generate_template()
    print(f"Generated {len(services)} service workspaces and template files.")


if __name__ == "__main__":
    main()
