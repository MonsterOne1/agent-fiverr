import unittest
import tempfile
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
        evidence = {check: f"evidence for {check}" for check in service.qa_checks}
        result = self.evaluator.evaluate(service.slug, payload, rubric_evidence=evidence)
        self.assertEqual(result.status, "pass")
        self.assertGreaterEqual(result.score, 4)

    def test_escalates_complete_deliverable_missing_rubric_evidence(self):
        service = self.catalog.get_service("blog-article-writer")
        payload = {field: f"value for {field}" for field in service.output_fields}
        result = self.evaluator.evaluate(service.slug, payload)
        self.assertEqual(result.status, "human_review")
        self.assertEqual(result.score, 3)
        self.assertEqual(result.missing_rubric_checks, service.qa_checks)

    def test_escalates_high_risk_service_to_human_review(self):
        service = self.catalog.get_service("market-research-brief")
        payload = {field: f"value for {field}" for field in service.output_fields}
        evidence = {check: f"evidence for {check}" for check in service.qa_checks}
        result = self.evaluator.evaluate(service.slug, payload, risk_override="high", rubric_evidence=evidence)
        self.assertEqual(result.status, "human_review")
        self.assertIn("high risk", " ".join(result.reasons))

    def test_human_review_queue_records_review_items(self):
        queue = HumanReviewQueue()
        result = self.evaluator.evaluate("presentation-pitch-deck", {"narrative": "thin"}, risk_override="high")
        item = queue.enqueue("order-1", "presentation-pitch-deck", result)
        self.assertEqual(item.order_id, "order-1")
        self.assertEqual(item.status, "open")
        self.assertIsNotNone(item.sla_due_at)
        self.assertEqual(len(queue.items), 1)

    def test_human_review_assignment_and_decision_are_recorded(self):
        queue = HumanReviewQueue()
        result = self.evaluator.evaluate("presentation-pitch-deck", {"narrative": "thin"}, risk_override="high")
        item = queue.enqueue("order-1", "presentation-pitch-deck", result, sla_hours=4)

        assigned = queue.assign(item.review_id, "reviewer-a")
        self.assertEqual(assigned.status, "assigned")
        self.assertEqual(assigned.reviewer_id, "reviewer-a")
        self.assertIsNotNone(assigned.assigned_at)

        decided = queue.decide(
            item.review_id,
            decision="changes_requested",
            reviewer_id="reviewer-a",
            notes="Need stronger evidence and source notes.",
        )
        self.assertEqual(decided.status, "changes_requested")
        self.assertEqual(decided.decision.reviewer_id, "reviewer-a")
        self.assertEqual(len(queue.pending()), 0)

    def test_human_review_decision_requires_assignment_and_matching_reviewer(self):
        queue = HumanReviewQueue()
        result = self.evaluator.evaluate("presentation-pitch-deck", {"narrative": "thin"}, risk_override="high")
        item = queue.enqueue("order-1", "presentation-pitch-deck", result)

        with self.assertRaisesRegex(ValueError, "must be assigned"):
            queue.decide(item.review_id, decision="approved", reviewer_id="reviewer-a", notes="ok")

        queue.assign(item.review_id, "reviewer-a")
        with self.assertRaises(PermissionError):
            queue.decide(item.review_id, decision="approved", reviewer_id="reviewer-b", notes="ok")

    def test_human_review_queue_persists_round_trip(self):
        queue = HumanReviewQueue()
        result = self.evaluator.evaluate("presentation-pitch-deck", {"narrative": "thin"}, risk_override="high")
        item = queue.enqueue("order-1", "presentation-pitch-deck", result)
        queue.assign(item.review_id, "reviewer-a")
        queue.decide(item.review_id, decision="approved", reviewer_id="reviewer-a", notes="ready")

        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "reviews.json"
            queue.save(path)
            loaded = HumanReviewQueue.load(path)

        self.assertEqual(len(loaded.items), 1)
        self.assertEqual(loaded.items[0].status, "approved")
        self.assertEqual(loaded.items[0].qa_result.reasons, result.reasons)
        self.assertEqual(loaded.items[0].decision.notes, "ready")


if __name__ == "__main__":
    unittest.main()
