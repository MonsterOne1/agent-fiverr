import tempfile
import unittest
from pathlib import Path

from agent_fiverr.qa import HumanReviewQueue, QAResult
from agent_fiverr.reviewers import ReviewerPool


ROOT = Path(__file__).resolve().parents[1]


class ReviewerPoolTest(unittest.TestCase):
    def test_loads_example_reviewer_pool(self):
        pool = ReviewerPool.load(ROOT)
        self.assertGreaterEqual(len(pool.reviewers), 4)
        self.assertTrue(all(reviewer.active for reviewer in pool.reviewers))

    def test_assigns_review_to_matching_specialty(self):
        pool = ReviewerPool.load(ROOT)
        queue = HumanReviewQueue()
        item = queue.enqueue(
            "order-1",
            "data-cleaning-formatting",
            QAResult(
                service_slug="data-cleaning-formatting",
                status="human_review",
                score=3,
                missing_fields=(),
                reasons=("rubric evidence missing",),
            ),
        )
        decision = pool.assign(queue, item.review_id)
        self.assertEqual(decision.reviewer_id, "qa-data-1")
        self.assertEqual(decision.reason, "specialty_match")
        self.assertEqual(queue.items[0].status, "assigned")

    def test_assignment_respects_reviewer_capacity(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "reviewers.json"
            path.write_text(
                """
[
  {"reviewer_id":"qa-data-1","name":"Data","specialties":["Data"],"max_open_reviews":1,"active":true},
  {"reviewer_id":"qa-general-1","name":"General","specialties":["general"],"max_open_reviews":2,"active":true}
]
""".strip()
                + "\n",
                encoding="utf-8",
            )
            pool = ReviewerPool.load(ROOT, path=path)
            queue = HumanReviewQueue()
            first = queue.enqueue(
                "order-1",
                "data-cleaning-formatting",
                QAResult("data-cleaning-formatting", "human_review", 3, (), ("review",)),
            )
            second = queue.enqueue(
                "order-2",
                "data-cleaning-formatting",
                QAResult("data-cleaning-formatting", "human_review", 3, (), ("review",)),
            )
            self.assertEqual(pool.assign(queue, first.review_id).reviewer_id, "qa-data-1")
            self.assertEqual(pool.assign(queue, second.review_id).reviewer_id, "qa-general-1")


if __name__ == "__main__":
    unittest.main()
