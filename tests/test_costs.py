import unittest
from pathlib import Path

from agent_fiverr.catalog import Catalog
from agent_fiverr.costs import estimate_service_cost, run_cost_gate


ROOT = Path(__file__).resolve().parents[1]


class CostGateTest(unittest.TestCase):
    def test_cost_gate_passes_for_all_mvp_services(self):
        summary, estimates = run_cost_gate(ROOT)
        self.assertTrue(summary.gate_pass)
        self.assertEqual(summary.services_checked, 20)
        self.assertEqual(len(estimates), 20)
        self.assertLessEqual(summary.max_cost_ratio, 0.30)

    def test_cost_estimate_includes_provider_and_automation_overhead(self):
        service = Catalog(ROOT).get_service("video-caption-repurpose")
        estimate = estimate_service_cost(service)
        self.assertEqual(estimate.package, "standard")
        self.assertGreater(estimate.estimated_cost_usd, 0)
        self.assertLessEqual(estimate.cost_ratio, 0.30)


if __name__ == "__main__":
    unittest.main()
