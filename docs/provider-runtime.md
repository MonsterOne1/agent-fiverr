# Provider Runtime

The provider runtime turns API requirements into executable gates before real
keys are available.

## Implemented

- Reads provider metadata from `data/api-provider-matrix.json`.
- Reports missing credentials per service without calling real providers.
- Supports dry-run provider actions for video, image, music, voiceover, coding,
  marketing, CMS, e-commerce, and research providers.
- Rejects provider actions that are not allowed for the selected service.
- Blocks non-dry-run provider actions when the required environment key is not
  configured.
- Emits provider traces with provider ID, action, side-effect level, request
  keys, and asset-manifest notes.

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
adapter is implemented. Required env var names are listed in
`data/api-provider-matrix.json`.

