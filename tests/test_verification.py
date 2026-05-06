import unittest
from pathlib import Path

from scripts.run_all_gates import GATE_COMMANDS


ROOT = Path(__file__).resolve().parents[1]


class VerificationGateTest(unittest.TestCase):
    def test_all_required_gate_commands_are_registered(self):
        commands = {" ".join(command) for command in GATE_COMMANDS}
        required = {
            "python3 scripts/validate_catalog.py",
            "python3 scripts/run_pilot_simulation.py",
            "python3 scripts/run_phase2_simulation.py",
            "python3 scripts/run_alpha_metrics.py",
            "python3 scripts/run_cost_gate.py",
            "python3 scripts/generate_long_tail_catalog.py",
            "python3 scripts/generate_eval_fixtures.py",
            "python3 -m unittest discover -s tests -p test_*.py",
            "git diff --check",
        }
        self.assertEqual(required - commands, set())

    def test_github_workflow_runs_local_gate_script(self):
        workflow = (ROOT / ".github" / "workflows" / "verify.yml").read_text(encoding="utf-8")
        self.assertIn("python3 scripts/run_all_gates.py", workflow)
        self.assertIn("actions/setup-python@v5", workflow)


if __name__ == "__main__":
    unittest.main()
