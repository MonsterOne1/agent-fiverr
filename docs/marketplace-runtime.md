# Marketplace Runtime

The marketplace runtime is a local alpha kernel for the plan's marketplace
layer. It is not a hosted UI or real payment system yet.

## Implemented

- Discover services by category or task type.
- Generate quotes from service slug, package, automation level, and brief
  completeness.
- Reject quotes with missing required brief fields.
- Accept ready quotes and create local workroom orders.
- Create escrow holds with buyer ID, quote ID, order ID, amount, provider,
  and hold ID.
- Keep the default local mock escrow compatible with current alpha checkout.
- Provide a Stripe Connect escrow scaffold with credential checks and call
  plans, without creating external payment objects.
- Expose discovery, quote, and quote acceptance through `agent_fiverr.cli`.

## Evidence

```text
python3 -m unittest discover -s tests -p 'test_marketplace.py'
Ran 5 tests
OK

python3 -m unittest discover -s tests -p 'test_payments.py'
Ran 5 tests
OK

python3 -m unittest discover -s tests -p 'test_cli.py'
Ran 4 tests
OK
```

## Remaining Work

- Buyer-facing web UI.
- Live Stripe Connect payment intent/capture/transfer calls after provider
  approval and `STRIPE_SECRET_KEY` setup.
- Refund/cancellation metrics.
- Dispute handling.
- Production persistence beyond local JSON workrooms.
