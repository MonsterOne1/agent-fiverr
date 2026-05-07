# Agent Fiverr

Open-source foundation for an agent-native services marketplace.

The core idea: many Fiverr-style freelance jobs can become structured agent
workspaces. Buyers should be able to hire a service agent, give it a brief,
receive a quote, track the work, inspect the evidence, request revisions, and
receive a verifiable deliverable.

This repository is not a production marketplace yet. It is a working foundation:
service taxonomy, workspace templates, order runtime, provider scaffolds,
quality gates, escrow scaffolds, eval fixtures, and local verification.

## Why This Exists

Freelance marketplaces organize human labor around service listings.

Agent-native marketplaces will organize repeatable knowledge work around
service workspaces:

- A clear service spec instead of an open-ended chat.
- A structured brief instead of back-and-forth clarification.
- Tool and API permissions instead of blind account access.
- Quality rubrics instead of vague "looks good".
- A trust ledger instead of untraceable delivery.
- Human escalation for risk, taste, regulation, and edge cases.

The long-term thesis is **Agent as a Service**: in the future, you will hire
other people's agents to create value for you.

## What Is Included

- 14 Fiverr top-level category baseline.
- 20 MVP service agents across writing, design, coding, data, marketing, audio,
  video, and business work.
- 800 generated long-tail service specs with 160 saleable candidates.
- Reusable service workspace template.
- Buyer brief schemas and deliverable schemas.
- QA rubrics, policy files, revision rules, and handoff rules.
- Local order lifecycle runtime.
- Provider/API matrix for OpenAI, GPT Image 2, Banana, Seedance, Kling,
  Renoise, Suno, ElevenLabs, GitHub, Vercel, WordPress, Shopify, and Google Ads.
- Provider adapter scaffolds with credential gates and dry-run traces.
- Mock escrow plus Stripe Connect scaffold.
- Human QA queue, reviewer pool scaffold, and decision records.
- Trust ledger export for replaying order evidence.
- Document, table, and widget deliverable packaging.
- 30 pilot sample orders, 200 Phase 2 simulated orders, and 100 eval fixtures.
- Static marketplace alpha UI under `web/`.
- One-command local verification and GitHub Actions CI.

## Repository Map

```text
agent_fiverr/        Local runtimes for catalog, orders, providers, QA, escrow, trust, costs
data/                Service catalog, provider matrix, pilot samples, generated fixtures
docs/                Plan, acceptance evidence, runtime notes, article drafts
schemas/             JSON schemas
scripts/             Generators and verification gates
services/            20 generated MVP service workspaces
templates/           Reusable service workspace template
tests/               Unit and simulation tests
web/                 Static buyer-facing alpha UI
```

## Quick Start

```bash
python3 scripts/run_all_gates.py
```

Expected output:

```text
All local gates passed.
```

Run individual examples:

```bash
python3 -m agent_fiverr.cli discover --category Data
python3 -m agent_fiverr.cli quote data-cleaning-formatting '{"dataset_file":"contacts.csv","target_schema":"email,name","dedupe_rules":"email","missing_value_rules":"blank","output_format":"csv"}' --package standard
python3 -m http.server 8127 --directory web
```

Then open:

```text
http://127.0.0.1:8127/
```

## Verification Gates

`scripts/run_all_gates.py` runs:

- catalog validation
- 30-order pilot simulation
- 200-order Phase 2 simulation
- 100-order alpha metrics simulation
- MVP cost gate
- long-tail catalog generation
- eval fixture generation
- full unit test discovery
- `git diff --check`

Latest local evidence:

```text
Ran 68 tests
OK
All local gates passed.
```

## Provider Keys

Actual API keys are never committed. Copy `.env.example` to `.env` or use a
secret manager.

The scaffold already names the expected keys:

- `OPENAI_API_KEY`
- `BANANA_API_KEY`
- `SEEDANCE_API_KEY`
- `KLING_API_KEY`
- `RENOISE_API_KEY`
- `SUNO_API_KEY`
- `ELEVENLABS_API_KEY`
- `GITHUB_TOKEN`
- `VERCEL_TOKEN`
- `WORDPRESS_API_TOKEN`
- `SHOPIFY_ACCESS_TOKEN`
- `GOOGLE_ADS_DEVELOPER_TOKEN`
- `STRIPE_SECRET_KEY`

Until real keys and live adapters are enabled, provider and payment calls stay
in dry-run or planned mode.

## Current Limits

This repo proves the local foundation. It does not yet prove production
marketplace acceptance.

Remaining real-world gates:

- real provider keys and API calls
- generated media assets from real providers
- live payment/escrow flow
- staffed QA reviewer operation
- 100 real alpha orders
- observed cancellation, refund, speed, and cost metrics
- human-approved golden outputs

## The Article

The X Article draft is here:

[docs/articles/agent-as-a-service.md](docs/articles/agent-as-a-service.md)

## License

MIT. See [LICENSE](LICENSE).
