# Long-Tail Catalog

The long-tail catalog generator supports Phase 4 expansion beyond the first 20
MVP services.

## Implemented

- Generates long-tail service spec drafts from the 20 MVP base services.
- Produces 800 generated service specs.
- Marks 160 saleable candidates.
- Ensures every generated service has a minimum eval pack:
  - `brief`
  - `expected_outline`
  - `qa_checklist`
  - `policy_expectations`

## Run

```bash
python3 scripts/generate_long_tail_catalog.py
```

Expected output:

```text
Long-tail catalog generated.
Service specs: 800
Saleable candidates: 160
Gate: PASS
```

## Output

```text
data/long-tail-services.generated.json
```

## Remaining Work

- Curate generated services with demand data.
- Promote validated service specs into real service workspaces.
- Add provider-specific adapters and real eval fixtures for each promoted
  long-tail service.

