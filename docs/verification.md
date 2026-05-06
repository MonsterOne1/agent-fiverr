# Verification

The local acceptance gates are now executable through one command and mirrored
in GitHub Actions.

## Command

```bash
python3 scripts/run_all_gates.py
```

The runner executes:

- catalog validation
- 30-order pilot simulation
- 200-order Phase 2 simulation
- 100-order alpha metrics simulation
- MVP cost gate
- long-tail catalog generation
- eval fixture generation
- full unit test discovery
- `git diff --check`

## CI

`.github/workflows/verify.yml` runs the same command on pushes to `main`,
pushes to `codex/phase0-service-foundation`, and pull requests.

## Remaining Work

- Add provider-key smoke tests once real API keys are available.
- Add hosted deployment checks once the alpha becomes a hosted app.
- Add real-order metric checks after pilot traffic exists.
