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
| Document key handoff without committing secrets | `.env.example` and `docs/credential-onboarding.md` | Tests check every provider/payment credential has an empty placeholder |
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
| Phase 2 sample baseline: 20 MVP agents each have at least 10 sample orders | `agent_fiverr/phase2_samples.py` | `scripts/run_phase2_simulation.py` generates 200 orders, 10 per MVP service, advances all to delivery, and emits provider dry-run traces |
| Provider/API requirements are executable without keys | `agent_fiverr/providers.py` and `docs/provider-runtime.md` | Provider runtime reports missing credentials, validates provider actions and request fields, emits call plans, blocks real calls without keys, and supports dry-run traces |
| Automatic QA and human review loop has executable baseline | `agent_fiverr/qa.py` and `docs/qa-runtime.md` | QA runtime blocks incomplete deliverables, escalates high-risk work, assigns reviewers, records decisions, persists review queues, and evaluates all 200 Phase 2 sample orders |
| Marketplace alpha kernel exists | `agent_fiverr/marketplace.py`, `agent_fiverr/payments.py`, and `docs/marketplace-runtime.md` | Unit tests cover service discovery, quote readiness, package price/SLA, order creation, mock escrow hold, Stripe Connect payment scaffold, and CLI buyer flow |
| Buyer-facing marketplace/workroom alpha UI exists | `web/` and `docs/web-alpha.md` | Static tests cover required regions and 20 MVP services; headless Chrome screenshots verify desktop and mobile rendering |
| Marketplace alpha metrics thresholds are executable | `agent_fiverr/alpha_metrics.py` and `docs/alpha-metrics.md` | `scripts/run_alpha_metrics.py` simulates 100 orders and checks cancellation, refund, response, and delivery-speed gates |
| Phase 4 long-tail expansion gate is executable | `agent_fiverr/long_tail.py`, `data/long-tail-services.generated.json`, and `docs/long-tail-catalog.md` | Generator produces 800 service specs, 160 saleable candidates, and minimum eval pack references for every service |

## Current Validator

Run:

```bash
python3 scripts/validate_catalog.py
python3 scripts/run_pilot_simulation.py
python3 scripts/run_phase2_simulation.py
python3 scripts/run_alpha_metrics.py
python3 scripts/generate_long_tail_catalog.py
```

Expected output:

```text
Catalog validation passed.
Top-level categories: 14
MVP services: 20
Providers: 14
Provider adapters: 14
Pilot sample orders: 30
Required files per service: 11

Pilot simulation passed.
Total orders: 30
Delivered orders: 30
Services: data-cleaning-formatting, presentation-pitch-deck, seo-geo-audit

Phase 2 simulation passed.
Total orders: 200
Delivered orders: 200
Services: 20
Provider dry-run traces: 460
QA evaluations: 200
Human review items: 0

Alpha metrics simulation
Total orders: 100
Cancellation rate: 7.0%
Refund rate: 3.0%
Average first response: 34.6s
Delivery speed improvement: 93.5%
Gate: PASS

Long-tail catalog generated.
Service specs: 800
Saleable candidates: 160
Gate: PASS
```

## Remaining Beyond Current Local Alpha

- Local order runner and static workroom UI are implemented, but hosted
  production persistence and real buyer accounts are not.
- No API keys are configured yet.
- Golden samples are named across all 20 services; simulations create structured
  sample orders and schema-complete placeholder deliverables, but these are not
  yet expanded into real expected output files.
- Automatic quality scoring has an executable baseline, but service-specific
  rubrics still need deeper scoring beyond required-field validation and risk
  escalation.
- Phase 2 now has 10 generated lifecycle samples per MVP service, but these are
  synthetic runtime simulations with provider dry-run traces. They still need
  real expected outputs, real provider adapters once keys are supplied, and
  service-specific quality scoring beyond required-field checks.
- Phase 3 metrics have executable simulated gates, but still require real buyer
  orders, real payments/escrow, cancellation/refund tracking, and human QA pool.
- Phase 4 long-tail specs are generated drafts. They need demand ranking,
  curation, provider adapter selection, and real eval fixtures before listing.
