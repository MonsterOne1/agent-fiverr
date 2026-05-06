# Reviewer Pool

The human QA workflow now has a local reviewer-pool scaffold for assigning
review items before a real staffing system or notification integration exists.

## Implemented

- Example reviewer roster in `data/reviewer-pool.example.json`.
- Reviewer specialties can match service slug or top-level category.
- Assignment chooses active reviewers with available capacity.
- Specialty matches are preferred; otherwise the pool falls back to general
  capacity.
- Assigned reviews are written back into `HumanReviewQueue`.

## Evidence

```text
python3 -m unittest discover -s tests -p 'test_reviewers.py'
Ran 3 tests
OK
```

## Remaining Work

- Replace example reviewers with real reviewer accounts.
- Add reviewer dashboard, notifications, availability windows, and audit
  approvals.
- Track reviewer quality and turnaround from real orders.
