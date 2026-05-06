# Phase 0/1 Acceptance Checklist

Date: 2026-05-06

## Objective

Turn the Agent Fiverr plan into concrete, auditable artifacts for category
coverage, service specs, workspace templates, provider/API requirements, and
catalog validation.

## Acceptance Evidence

| Requirement | Evidence | Verification |
|---|---|---|
| Cover 100% top-level Fiverr categories from the plan | `data/top-level-categories.json` contains 14 top-level categories | `python3 scripts/validate_catalog.py` checks category count >= 14 |
| Define `service_spec` schema | `schemas/service_spec.schema.json` | File exists and required fields are mirrored in validator |
| Map services to task type, automation level, risk, tools, deliverables | `data/mvp-services.json` | Validator checks every service has these fields |
| Capture API/provider requirements by task type | `data/api-provider-matrix.json` | Validator checks every referenced provider exists |
| Include owner-named APIs for media work | Seedance/Kling/Renoise for video, Banana/GPT Image 2 for image/design, Suno for music, ElevenLabs for voiceover/TTS | Provider matrix and relevant service specs reference these providers |
| Produce 20 MVP service specs | `services/<slug>/` for 20 services | Validator checks exactly 20 services and generated workspaces |
| Each MVP service has brief schema | `services/<slug>/BRIEF_SCHEMA.json` | Validator checks brief fields are required |
| Each MVP service has deliverable schema | `services/<slug>/DELIVERABLE_SCHEMA.json` | Validator checks output fields are required |
| Each MVP service has QA rubric | `services/<slug>/QA_RUBRIC.md` | Validator checks required file set |
| Each MVP service has policy | `services/<slug>/POLICY.md` | Validator checks required file set and authorization language for side-effect providers |
| Create reusable agent service template | `templates/agent-service-template/` | Validator checks full required file set |
| Define lifecycle/state-machine baseline | `WORKSPACE_MANIFEST.json` in template and generated service dirs | Validator checks lifecycle sequence |
| External side effects require explicit authorization | `POLICY.md` and `WORKSPACE_MANIFEST.json` | Validator checks policy text for services using side-effect providers |
| Seed first 3 pilot agents with 30 simulated orders | `data/pilot-sample-orders.json` | Validator checks exactly 30 samples, 10 each for SEO audit, data cleaning, and presentation deck |
| Run first 3 pilot agents through local order lifecycle | `scripts/run_pilot_simulation.py` | Simulation creates 30 temporary workroom orders, advances them to delivery, and adds QA-passing deliverables |

## Current Validator

Run:

```bash
python3 scripts/validate_catalog.py
python3 scripts/run_pilot_simulation.py
```

Expected output:

```text
Catalog validation passed.
Top-level categories: 14
MVP services: 20
Providers: 14
Pilot sample orders: 30
Required files per service: 11

Pilot simulation passed.
Total orders: 30
Delivered orders: 30
Services: data-cleaning-formatting, presentation-pitch-deck, seo-geo-audit
```

## Remaining Beyond Phase 0/1

- Real order runner and workroom UI are not implemented.
- No API keys are configured yet.
- Golden samples are named across all 20 services; the first three pilot agents
  have 30 structured seed sample orders, but these are not yet expanded into
  full expected output files.
- Automatic quality scoring exists as rubric text, not an executable evaluator.
- Phase 2 requires 10-20 sample orders per MVP service.
- Phase 3 requires real buyer orders, payments/escrow, cancellation/refund
  tracking, and human QA pool.
