import unittest

from agent_fiverr.phase2_samples import generate_phase2_sample_orders, run_phase2_simulation


class Phase2SamplesTest(unittest.TestCase):
    def test_generates_10_sample_orders_for_each_mvp_service(self):
        samples = generate_phase2_sample_orders()
        self.assertEqual(len(samples), 200)
        counts = {}
        for sample in samples:
            counts[sample["service_slug"]] = counts.get(sample["service_slug"], 0) + 1
            self.assertIn("sample_id", sample)
            self.assertTrue(sample["brief"])
            self.assertTrue(sample["expected_deliverables"])
            self.assertTrue(sample["qa_expectations"])
            self.assertTrue(sample["policy_expectations"])
        self.assertEqual(len(counts), 20)
        self.assertTrue(all(count == 10 for count in counts.values()))

    def test_runs_all_mvp_sample_orders_through_lifecycle(self):
        summary = run_phase2_simulation()
        self.assertEqual(summary.total_orders, 200)
        self.assertEqual(summary.delivered_orders, 200)
        self.assertEqual(len(summary.services), 20)


if __name__ == "__main__":
    unittest.main()

