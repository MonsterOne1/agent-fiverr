import json
import tempfile
import unittest
from pathlib import Path

from agent_fiverr.catalog import Catalog
from agent_fiverr.order import OrderRuntime
from agent_fiverr.payments import EscrowRuntime
from agent_fiverr.providers import ProviderRuntime
from agent_fiverr.qa import QAEvaluator
from agent_fiverr.trust import build_trust_ledger


ROOT = Path(__file__).resolve().parents[1]


class TrustLedgerTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        for dirname in ["data", "services"]:
            (self.root / dirname).symlink_to(ROOT / dirname, target_is_directory=True)
        self.catalog = Catalog(self.root)
        self.runtime = OrderRuntime(self.root, self.catalog)

    def tearDown(self):
        self.tmp.cleanup()

    def test_trust_ledger_replays_order_provider_qa_and_escrow_records(self):
        service = self.catalog.get_service("seo-geo-audit")
        order = self.runtime.create_order(service.slug, {
            "website_url": "https://example.com",
            "target_market": "US",
            "target_keywords": "ai notes",
            "competitors": "competitor a",
            "cms": "Webflow",
            "business_goal": "increase demos",
        })
        for state in ["scope_check", "quote", "plan", "work", "qa"]:
            self.runtime.transition(order, state)

        payload = {field: f"value for {field}" for field in service.output_fields}
        evidence = {check: f"evidence for {check}" for check in service.qa_checks}
        qa_result = QAEvaluator(self.catalog).evaluate(service.slug, payload, rubric_evidence=evidence)
        self.runtime.add_deliverable(order, payload, qa_score=qa_result.score, qa_notes=list(qa_result.reasons))
        provider_trace = ProviderRuntime(self.catalog).run(
            service.slug,
            "browser_search",
            "simulate_provider_output",
            {"sample_id": "seo-001"},
            dry_run=True,
        )
        hold = EscrowRuntime().hold_funds(
            order_id=order.order_id,
            quote_id="quote-1",
            buyer_id="buyer-1",
            amount_usd=150,
        )
        release = EscrowRuntime().release_funds(hold, authorization_id="buyer-accepted")

        ledger = build_trust_ledger(
            order,
            provider_traces=[provider_trace],
            escrow_events=[hold, release],
            qa_results=[qa_result],
        )

        self.assertEqual(ledger.order_id, order.order_id)
        self.assertEqual(ledger.replay_counts["provider_traces"], 1)
        self.assertEqual(ledger.replay_counts["escrow_events"], 2)
        self.assertEqual(ledger.replay_counts["qa_results"], 1)
        self.assertEqual(ledger.deliverable_versions[0]["version"], 1)

    def test_trust_ledger_saves_json_artifact(self):
        order = self.runtime.create_order("seo-geo-audit", {
            "website_url": "https://example.com",
            "target_market": "US",
            "target_keywords": "ai notes",
            "competitors": "competitor a",
            "cms": "Webflow",
            "business_goal": "increase demos",
        })
        ledger = build_trust_ledger(order)
        path = self.root / "ledger" / "order.json"
        ledger.save(path)

        payload = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(payload["order_id"], order.order_id)
        self.assertEqual(payload["replay_counts"]["audit_events"], 1)


if __name__ == "__main__":
    unittest.main()
