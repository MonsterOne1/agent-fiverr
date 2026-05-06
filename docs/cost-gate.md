# Cost Gate

The platform-level plan requires agent fulfillment cost to stay below roughly
20%-30% of service price. This runtime adds a local simulation gate for the 20
MVP services.

## Implemented

- Estimates standard-package cost from provider/API cost assumptions,
  automation-level overhead, and package multiplier.
- Compares every MVP service against a 30% maximum cost-ratio gate.
- Exposes a script gate for CI/local checks.

## Evidence

```text
python3 scripts/run_cost_gate.py
Cost gate simulation
Services checked: 20
Package: standard
Threshold: 30%
Max cost ratio: 18.4%
Gate: PASS

python3 -m unittest discover -s tests -p 'test_costs.py'
Ran 2 tests
OK
```

## Remaining Work

- Replace simulated provider costs with observed provider invoices once real
  API calls are enabled.
- Track per-order token/media/render cost in the order audit ledger.
- Compare actual margin by service, package, revision count, and provider.
