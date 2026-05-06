import unittest

from agent_fiverr.pilot_simulation import run_pilot_simulation


class PilotSimulationTest(unittest.TestCase):
    def test_runs_30_pilot_orders(self):
        summary = run_pilot_simulation()
        self.assertEqual(summary.total_orders, 30)
        self.assertEqual(summary.delivered_orders, 30)
        self.assertEqual(
            summary.services,
            ("data-cleaning-formatting", "presentation-pitch-deck", "seo-geo-audit"),
        )


if __name__ == "__main__":
    unittest.main()

