# QA Runtime

The QA runtime implements the first executable version of the plan's automatic
evaluation and human-review loop.

## Implemented

- Checks deliverable payloads against each service's required output fields.
- Blocks delivery when required fields are missing.
- Produces a numeric QA score.
- Escalates high-risk work to human review.
- Provides an in-memory human review queue for order-level escalation.
- Integrates with the Phase 2 simulation so all 200 generated MVP sample orders
  receive automatic QA evaluation before delivery.

## Evidence

```text
python3 -m unittest discover -s tests -p 'test_qa_runtime.py'
Ran 4 tests
OK

python3 scripts/run_phase2_simulation.py
QA evaluations: 200
```

## Remaining Work

- Service-specific scoring rubrics beyond required-field validation.
- Human reviewer assignment, SLA, and decision recording.
- Quality metrics aggregation across real orders.
- Eval fixtures with expected outputs for all 20 MVP services.

