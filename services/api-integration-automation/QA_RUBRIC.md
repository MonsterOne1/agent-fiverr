# QA Rubric

## Required Checks

- auth_secrets_not_committed
- idempotency_considered
- external_side_effects_authorized

## Universal Checks

- Brief is complete or missing fields are listed as assumptions.
- Deliverable matches `DELIVERABLE_SCHEMA.json`.
- Provider/API outputs are logged in `TOOLS.md` or the order trace.
- High-risk claims and side effects are escalated before delivery.

## Scoring

- 5: Ready to deliver with no material issues.
- 4: Ready with minor notes.
- 3: Needs revision before delivery.
- 2: Requires human review.
- 1: Out of scope or unsafe.

Delivery threshold: 4 or higher.
