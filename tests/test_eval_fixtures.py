import json
import unittest
from pathlib import Path

from agent_fiverr.eval_fixtures import generate_eval_fixtures, validate_eval_fixtures


ROOT = Path(__file__).resolve().parents[1]


class EvalFixturesTest(unittest.TestCase):
    def test_generates_five_eval_fixtures_for_each_mvp_service(self):
        fixtures = generate_eval_fixtures(ROOT)
        summary = validate_eval_fixtures(fixtures, ROOT)
        self.assertEqual(summary.total_fixtures, 100)
        self.assertEqual(summary.services, 20)
        self.assertEqual(summary.fixtures_per_service, 5)

    def test_generated_fixture_artifact_is_valid(self):
        path = ROOT / "data" / "eval-fixtures.generated.json"
        fixtures = json.loads(path.read_text(encoding="utf-8"))
        summary = validate_eval_fixtures(fixtures, ROOT)
        self.assertEqual(summary.total_fixtures, 100)


if __name__ == "__main__":
    unittest.main()
