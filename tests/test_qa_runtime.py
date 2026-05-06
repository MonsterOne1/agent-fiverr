import unittest
from pathlib import Path

from agent_fiverr.catalog import Catalog
from agent_fiverr.qa import HumanReviewQueue, QAEvaluator


ROOT = Path(__file__).resolve().parents[1]


class QARuntimeTest(unittest.TestCase):
    def setUp(self):
        self.catalog = Catalog(ROOT)
        self.evaluator = QAEvaluator(self.catalog)

    def test_blocks_deliverable_missing_required_output_fields(self):
        result = self.evaluator.evaluate("seo-geo-audit", {"executive_summary": "summary"})
        self.assertEqual(result.status, "block")
        self.assertLess(result.score, 4)
        self.assertIn("technical_findings", result.missing_fields)

    def test_passes_complete_low_risk_deliverable(self):
        service = self.catalog.get_service("blog-article-writer")
        payload = {field: f"value for {field}" for field in service.output_fields}
        result = self.evaluator.evaluate(service.slug, payload)
        self.assertEqual(result.status, "pass")
        self.assertGreaterEqual(result.score, 4)

    def test_escalates_high_risk_service_to_human_review(self):
        service = self.catalog.get_service("market-research-brief")
        payload = {field: f"value for {field}" for field in service.output_fields}
        result = self.evaluator.evaluate(service.slug, payload, risk_override="high")
        self.assertEqual(result.status, "human_review")
        self.assertIn("high risk", " ".join(result.reasons))

    def test_human_review_queue_records_review_items(self):
        queue = HumanReviewQueue()
        result = self.evaluator.evaluate("presentation-pitch-deck", {"narrative": "thin"}, risk_override="high")
        item = queue.enqueue("order-1", "presentation-pitch-deck", result)
        self.assertEqual(item.order_id, "order-1")
        self.assertEqual(item.status, "open")
        self.assertEqual(len(queue.items), 1)


if __name__ == "__main__":
    unittest.main()

