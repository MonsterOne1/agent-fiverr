# Trust Ledger

The plan requires traceability: replaying orders, tool calls, file versions, and
decisions. The trust ledger exports those records into one JSON artifact.

## Implemented

- Exports order audit events and lifecycle state.
- Exports deliverable versions and revision requests.
- Accepts provider traces from the provider runtime.
- Accepts QA results from the QA runtime.
- Accepts escrow holds/actions from the payment runtime.
- Writes a replayable JSON artifact with counts for each evidence stream.

## Evidence

```text
python3 -m unittest discover -s tests -p 'test_trust.py'
Ran 2 tests
OK
```

## Remaining Work

- Attach trust ledger export to every hosted production order automatically.
- Store generated files/assets beside the ledger with immutable references.
- Add signed ledger snapshots for real buyer disputes and compliance review.
