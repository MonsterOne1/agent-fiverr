import os
import unittest
from pathlib import Path

from agent_fiverr.catalog import Catalog
from agent_fiverr.providers import ProviderRuntime


ROOT = Path(__file__).resolve().parents[1]


class ProviderRuntimeTest(unittest.TestCase):
    def setUp(self):
        self.catalog = Catalog(ROOT)
        self.runtime = ProviderRuntime(self.catalog)

    def test_reports_missing_credentials_without_calling_real_provider(self):
        report = self.runtime.credential_report("video-caption-repurpose")
        missing = {item.provider_id for item in report if item.required and not item.configured}
        self.assertIn("seedance", missing)
        self.assertIn("elevenlabs", missing)

    def test_dry_run_provider_action_records_trace_and_asset_manifest(self):
        trace = self.runtime.run(
            "video-caption-repurpose",
            "seedance",
            "generate_video",
            {"prompt": "short product video"},
            dry_run=True,
        )
        self.assertEqual(trace.provider_id, "seedance")
        self.assertEqual(trace.status, "dry_run")
        self.assertEqual(trace.side_effect_level, "asset_generation")
        self.assertEqual(trace.asset_manifest["provider"], "seedance")
        self.assertEqual(trace.asset_manifest["action"], "generate_video")

    def test_real_provider_action_requires_configured_key(self):
        old_value = os.environ.pop("SEEDANCE_API_KEY", None)
        try:
            with self.assertRaises(PermissionError):
                self.runtime.run(
                    "video-caption-repurpose",
                    "seedance",
                    "generate_video",
                    {"prompt": "short product video"},
                    dry_run=False,
                )
        finally:
            if old_value is not None:
                os.environ["SEEDANCE_API_KEY"] = old_value

    def test_rejects_provider_not_allowed_for_service(self):
        with self.assertRaises(ValueError):
            self.runtime.run(
                "blog-article-writer",
                "seedance",
                "generate_video",
                {"prompt": "not allowed"},
                dry_run=True,
            )


if __name__ == "__main__":
    unittest.main()

