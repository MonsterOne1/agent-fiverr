# Marketplace Runtime

The marketplace runtime is a local alpha kernel for the plan's marketplace
layer. It is not a hosted UI or real payment system yet.

## Implemented

- Discover services by category or task type.
- Generate quotes from service slug, package, automation level, and brief
  completeness.
- Reject quotes with missing required brief fields.
- Accept ready quotes and create local workroom orders.
- Create a mock escrow hold with buyer ID, quote ID, order ID, and amount.

## Evidence

```text
python3 -m unittest discover -s tests -p 'test_marketplace.py'
Ran 4 tests
OK
```

## Remaining Work

- Buyer-facing web UI.
- Real payments/escrow provider.
- Refund/cancellation metrics.
- Dispute handling.
- Production persistence beyond local JSON workrooms.

