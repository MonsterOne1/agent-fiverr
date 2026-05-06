# Phase 1 Runtime

This repo now includes a minimal local runtime for the plan's Phase 1 gates.

## Implemented

- Load service catalog and provider matrix.
- Validate buyer brief completeness against each service's required fields.
- Create a local workroom order under `workrooms/`.
- Enforce the lifecycle:
  `intake -> scope_check -> quote -> plan -> work -> qa -> delivery -> revision -> close -> memory`.
- Record audit events for order creation, state transitions, authorizations,
  blocked actions, deliverables, and revisions.
- Block configured provider side effects until explicit authorization is granted.
- Version deliverables and block delivery below QA threshold.
- Package document, table, and widget deliverables with per-order manifests.
- Classify revision requests as in-scope or scope-change candidates.
- Run the 30 seed pilot sample orders through the local lifecycle runtime.
- Run 200 generated Phase 2 sample orders: 10 for each MVP service.
- Emit provider dry-run traces for every provider required by every Phase 2
  sample order.
- Evaluate every Phase 2 deliverable with the QA runtime before delivery.

## Commands

```bash
python3 -m agent_fiverr.cli list-services
python3 -m agent_fiverr.cli validate-brief seo-geo-audit '{"website_url":"https://example.com"}'
python3 -m agent_fiverr.cli create-order seo-geo-audit '{"website_url":"https://example.com","target_market":"US","target_keywords":"ai notes","competitors":"a","cms":"Webflow","business_goal":"increase demos"}'
```

## Verification

```bash
python3 scripts/validate_catalog.py
python3 scripts/run_pilot_simulation.py
python3 scripts/run_phase2_simulation.py
python3 -m unittest discover -s tests -p 'test_*.py'
```

## Not Yet Implemented

- Actual agent execution against provider APIs.
- Hosted workroom UI.
- Hosted file storage and signed download URLs for deliverables.
- Real staffed expert marketplace.
