import json
import unittest
from pathlib import Path

from agent_fiverr.payments import EscrowRuntime


ROOT = Path(__file__).resolve().parents[1]


class CredentialOnboardingTest(unittest.TestCase):
    def test_env_example_covers_all_provider_and_payment_credentials(self):
        env_example = _load_env_example(ROOT / ".env.example")
        matrix = json.loads((ROOT / "data" / "api-provider-matrix.json").read_text(encoding="utf-8"))
        provider_envs = {
            provider["credential_env"]
            for provider in matrix["providers"]
            if provider.get("credential_env")
        }
        payment_envs = {
            item["credential_env"]
            for item in EscrowRuntime().provider_report()
            if item.get("credential_env")
        }

        missing = sorted((provider_envs | payment_envs) - set(env_example))
        self.assertEqual(missing, [])

    def test_env_example_contains_empty_placeholders_only(self):
        env_example = _load_env_example(ROOT / ".env.example")
        filled = {key: value for key, value in env_example.items() if value}
        self.assertEqual(filled, {})


def _load_env_example(path: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        key, _, value = line.partition("=")
        result[key] = value
    return result


if __name__ == "__main__":
    unittest.main()
