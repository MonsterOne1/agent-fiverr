import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class CLITest(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, "-m", "agent_fiverr.cli", *args],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_discover_outputs_marketplace_services(self):
        result = self.run_cli("discover", "--category", "Data")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("data-cleaning-formatting", result.stdout)

    def test_quote_outputs_ready_quote_json(self):
        brief = json.dumps({
            "dataset_file": "contacts.csv",
            "target_schema": "email,name",
            "dedupe_rules": "email",
            "missing_value_rules": "blank",
            "output_format": "csv",
        })
        result = self.run_cli("quote", "data-cleaning-formatting", brief, "--package", "standard")
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertTrue(payload["ready"])
        self.assertEqual(payload["price_usd"], 150)

    def test_accept_quote_creates_checkout_json(self):
        brief = json.dumps({
            "dataset_file": "contacts.csv",
            "target_schema": "email,name",
            "dedupe_rules": "email",
            "missing_value_rules": "blank",
            "output_format": "csv",
        })
        result = self.run_cli("accept-quote", "data-cleaning-formatting", brief, "--buyer-id", "buyer-1")
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["escrow_status"], "held")
        self.assertEqual(payload["escrow_provider"], "mock")
        self.assertEqual(payload["buyer_id"], "buyer-1")

    def test_accept_quote_supports_stripe_connect_scaffold(self):
        brief = json.dumps({
            "dataset_file": "contacts.csv",
            "target_schema": "email,name",
            "dedupe_rules": "email",
            "missing_value_rules": "blank",
            "output_format": "csv",
        })
        result = self.run_cli(
            "accept-quote",
            "data-cleaning-formatting",
            brief,
            "--buyer-id",
            "buyer-1",
            "--escrow-provider",
            "stripe_connect",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["escrow_status"], "planned")
        self.assertEqual(payload["escrow_provider"], "stripe_connect")


if __name__ == "__main__":
    unittest.main()
