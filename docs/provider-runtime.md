# Provider Runtime

The provider runtime turns API requirements into executable gates before real
keys are available.

## Implemented

- Reads provider metadata from `data/api-provider-matrix.json`.
- Registers an adapter scaffold for every provider in the matrix, including
  action names, required request fields, scopes, artifact types, and whether
  live calls are enabled.
- Reports missing credentials per service without calling real providers.
- Supports dry-run provider actions for video, image, music, voiceover, coding,
  marketing, CMS, e-commerce, and research providers.
- Rejects provider actions that are not allowed for the selected service.
- Rejects unsupported provider actions and requests missing action-specific
  fields before any credential check or network-capable step.
- Blocks non-dry-run provider actions when the required environment key is not
  configured.
- Emits provider traces with provider ID, action, side-effect level, request
  keys, adapter manifest, call plan, and asset-manifest notes.
- If a key is configured, non-dry-run mode returns a call plan with
  `live_call_status: not_implemented` until a provider adapter is deliberately
  enabled. This prevents accidental production calls while still documenting the
  required integration surface.

## Phase 2 Simulation

`scripts/run_phase2_simulation.py` now runs dry-run provider traces for every
provider required by every generated sample order.

Latest expected evidence:

```text
Phase 2 simulation passed.
Total orders: 200
Delivered orders: 200
Services: 20
Provider dry-run traces: 460
```

## Real Provider Cutover

Real calls remain disabled until keys are supplied and a service-specific
adapter is implemented and explicitly marked live-enabled. Required env var
names are listed in `data/api-provider-matrix.json`.
