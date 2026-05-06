import os
import unittest

from agent_fiverr.payments import EscrowRuntime, payment_provider_for


class PaymentRuntimeTest(unittest.TestCase):
    def test_mock_escrow_hold_is_held_without_credentials(self):
        runtime = EscrowRuntime()
        hold = runtime.hold_funds(
            order_id="order-1",
            quote_id="quote-1",
            buyer_id="buyer-1",
            amount_usd=150,
        )
        self.assertEqual(hold.provider_id, "mock")
        self.assertEqual(hold.status, "held")
        self.assertEqual(hold.mode, "mock")
        self.assertFalse(hold.credential_configured)

    def test_stripe_connect_dry_run_returns_call_plan(self):
        runtime = EscrowRuntime()
        hold = runtime.hold_funds(
            order_id="order-1",
            quote_id="quote-1",
            buyer_id="buyer-1",
            amount_usd=150,
            provider_id="stripe_connect",
            dry_run=True,
        )
        self.assertEqual(hold.provider_id, "stripe_connect")
        self.assertEqual(hold.status, "planned")
        self.assertEqual(hold.call_plan["credential_env"], "STRIPE_SECRET_KEY")
        self.assertEqual(hold.call_plan["live_call_status"], "dry_run")

    def test_stripe_connect_live_mode_requires_key(self):
        old_value = os.environ.pop("STRIPE_SECRET_KEY", None)
        try:
            with self.assertRaises(PermissionError):
                EscrowRuntime().hold_funds(
                    order_id="order-1",
                    quote_id="quote-1",
                    buyer_id="buyer-1",
                    amount_usd=150,
                    provider_id="stripe_connect",
                    dry_run=False,
                )
        finally:
            if old_value is not None:
                os.environ["STRIPE_SECRET_KEY"] = old_value

    def test_configured_stripe_key_still_keeps_live_calls_disabled(self):
        old_value = os.environ.get("STRIPE_SECRET_KEY")
        os.environ["STRIPE_SECRET_KEY"] = "sk_test_example"
        try:
            hold = EscrowRuntime().hold_funds(
                order_id="order-1",
                quote_id="quote-1",
                buyer_id="buyer-1",
                amount_usd=150,
                provider_id="stripe_connect",
                dry_run=False,
            )
        finally:
            if old_value is None:
                os.environ.pop("STRIPE_SECRET_KEY", None)
            else:
                os.environ["STRIPE_SECRET_KEY"] = old_value

        self.assertEqual(hold.status, "planned")
        self.assertTrue(hold.credential_configured)
        self.assertFalse(hold.call_plan["live_call_allowed"])
        self.assertEqual(hold.call_plan["live_call_status"], "not_implemented")

    def test_payment_provider_registry_exposes_capabilities(self):
        spec = payment_provider_for("stripe_connect")
        self.assertIn("manual_capture", spec.capabilities)
        self.assertEqual(spec.credential_env, "STRIPE_SECRET_KEY")


if __name__ == "__main__":
    unittest.main()
