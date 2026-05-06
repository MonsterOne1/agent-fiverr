import unittest

from agent_fiverr.alpha_metrics import AlphaMetricGate, run_alpha_metrics_simulation


class AlphaMetricsTest(unittest.TestCase):
    def test_simulates_100_alpha_orders_with_plan_thresholds(self):
        report = run_alpha_metrics_simulation()
        self.assertEqual(report.total_orders, 100)
        self.assertLess(report.cancellation_rate, 0.10)
        self.assertLess(report.refund_rate, 0.05)
        self.assertLess(report.average_first_response_seconds, 120)
        self.assertGreaterEqual(report.delivery_speed_improvement, 0.50)

    def test_metric_gate_passes_when_all_thresholds_are_met(self):
        report = run_alpha_metrics_simulation()
        result = AlphaMetricGate().evaluate(report)
        self.assertTrue(result.passed)
        self.assertEqual(result.failures, ())


if __name__ == "__main__":
    unittest.main()

