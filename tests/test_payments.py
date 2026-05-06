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

    def test_mock_escrow_release_requires_authorization_and_records_action(self):
        runtime = EscrowRuntime()
        hold = runtime.hold_funds(
            order_id="order-1",
            quote_id="quote-1",
            buyer_id="buyer-1",
            amount_usd=150,
        )
        with self.assertRaises(PermissionError):
            runtime.release_funds(hold, authorization_id="")

        action = runtime.release_funds(hold, authorization_id="buyer-acceptance-1")
        self.assertEqual(action.action, "release")
        self.assertEqual(action.status, "released")
        self.assertEqual(action.amount_usd, 150)
        self.assertEqual(action.authorization_id, "buyer-acceptance-1")

    def test_mock_escrow_refund_validates_amount_and_records_reason(self):
        runtime = EscrowRuntime()
        hold = runtime.hold_funds(
            order_id="order-1",
            quote_id="quote-1",
            buyer_id="buyer-1",
            amount_usd=150,
        )
        with self.assertRaises(ValueError):
            runtime.refund(hold, reason="duplicate", authorization_id="support-1", amount_usd=175)

        action = runtime.refund(hold, reason="buyer cancellation", authorization_id="support-1", amount_usd=75)
        self.assertEqual(action.action, "refund")
        self.assertEqual(action.status, "refunded")
        self.assertEqual(action.amount_usd, 75)
        self.assertEqual(action.reason, "buyer cancellation")

    def test_mock_escrow_dispute_requires_evidence(self):
        runtime = EscrowRuntime()
        hold = runtime.hold_funds(
            order_id="order-1",
            quote_id="quote-1",
            buyer_id="buyer-1",
            amount_usd=150,
        )
        with self.assertRaises(ValueError):
            runtime.open_dispute(hold, reason="quality disagreement", evidence_refs=())

        action = runtime.open_dispute(
            hold,
            reason="quality disagreement",
            evidence_refs=("workrooms/order-1/deliverable-v1.json",),
        )
        self.assertEqual(action.action, "dispute")
        self.assertEqual(action.status, "disputed")
        self.assertEqual(action.evidence_refs, ("workrooms/order-1/deliverable-v1.json",))

    def test_stripe_escrow_actions_remain_planned_until_live_enabled(self):
        runtime = EscrowRuntime()
        hold = runtime.hold_funds(
            order_id="order-1",
            quote_id="quote-1",
            buyer_id="buyer-1",
            amount_usd=150,
            provider_id="stripe_connect",
            dry_run=True,
        )
        action = runtime.release_funds(hold, authorization_id="buyer-acceptance-1")
        self.assertEqual(action.status, "planned")
        self.assertEqual(action.call_plan["escrow_action"], "release")


if __name__ == "__main__":
    unittest.main()
