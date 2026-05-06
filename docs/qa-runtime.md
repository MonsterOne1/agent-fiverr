# QA Runtime

The QA runtime implements the first executable version of the plan's automatic
evaluation and human-review loop.

## Implemented

- Checks deliverable payloads against each service's required output fields.
- Blocks delivery when required fields are missing.
- Requires evidence for every service-specific QA rubric check before automatic
  pass.
- Escalates schema-complete deliverables with missing rubric evidence to human
  review.
- Produces a numeric QA score.
- Escalates high-risk work to human review.
- Provides a human review queue for order-level escalation.
- Records reviewer assignment, SLA due time, reviewer-matched decisions, and
  decision notes.
- Supports JSON persistence/restore for review queues so review state can move
  beyond a single process.
- Integrates with the Phase 2 simulation so all 200 generated MVP sample orders
  receive automatic QA evaluation before delivery.

## Evidence

```text
python3 -m unittest discover -s tests -p 'test_qa_runtime.py'
Ran 8 tests
OK

python3 scripts/run_phase2_simulation.py
QA evaluations: 200
```

## Remaining Work

- Expert semantic scoring beyond rubric-evidence presence.
- Reviewer staffing, dashboards, and notification integrations.
- Quality metrics aggregation across real orders.
- Human-approved eval fixture expected outputs for priority services.
