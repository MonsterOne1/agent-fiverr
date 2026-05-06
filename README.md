# Agent Fiverr

Research, planning, and service-spec foundation for an agent-native Fiverr-style
marketplace.

## Current Artifacts

- `docs/agent-fiverr-plan.md` - original strategy and phased acceptance criteria.
- `data/top-level-categories.json` - Fiverr top-level category coverage map.
- `data/service-archetypes.json` - reusable service agent archetypes.
- `data/api-provider-matrix.json` - provider/API requirements, including Seedance,
  Banana, GPT Image 2, Suno, ElevenLabs, GitHub, Vercel, Shopify, WordPress, and
  other provider classes.
- `data/mvp-services.json` - 20 MVP service definitions.
- `data/pilot-sample-orders.json` - 30 seed sample orders for the first three
  pilot agents: SEO audit, data cleaning, and presentation deck.
- `agent_fiverr/phase2_samples.py` - generated 200-sample Phase 2 order set:
  10 sample orders for each of the 20 MVP services.
- `services/<service>/` - generated workspace spec for each MVP service.
- `templates/agent-service-template/` - reusable service workspace template.
- `schemas/` - JSON schemas for service specs and workspace manifests.
- `agent_fiverr/` - minimal local catalog/order runtime for Phase 1 gates.
- `tests/` - unit tests for catalog loading, brief validation, lifecycle,
  authorization gates, deliverable versioning, revision scope, provider dry-runs,
  and Phase 2 sample simulations.
- `scripts/generate_service_workspaces.py` - generates service workspaces from
  `data/mvp-services.json`.
- `scripts/validate_catalog.py` - validates Phase 0/1 catalog acceptance gates.

## Commands

```bash
python3 scripts/generate_service_workspaces.py
python3 scripts/validate_catalog.py
python3 scripts/run_pilot_simulation.py
python3 scripts/run_phase2_simulation.py
python3 -m unittest discover -s tests -p 'test_*.py'
```

## Credential Policy

Provider names and required credential environment variables are committed.
Actual API keys are never committed. The owner will provide keys later through
`.env`, a secret manager, or per-workspace provider authorization.
