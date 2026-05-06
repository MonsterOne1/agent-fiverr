import os
import unittest
from pathlib import Path

from agent_fiverr.catalog import Catalog
from agent_fiverr.providers import ProviderRuntime, adapter_for


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
            {
                "prompt": "short product video",
                "duration_seconds": 8,
                "aspect_ratio": "9:16",
                "usage_rights": "commercial_safe_generated_asset",
            },
            dry_run=True,
        )
        self.assertEqual(trace.provider_id, "seedance")
        self.assertEqual(trace.status, "dry_run")
        self.assertEqual(trace.side_effect_level, "asset_generation")
        self.assertEqual(trace.asset_manifest["provider"], "seedance")
        self.assertEqual(trace.asset_manifest["action"], "generate_video")
        self.assertIn("mp4", trace.asset_manifest["artifact_types"])
        self.assertIn("generate_video", trace.adapter["actions"])
        self.assertFalse(trace.call_plan["live_call_allowed"])
        self.assertEqual(trace.call_plan["live_call_status"], "dry_run")

    def test_real_provider_action_requires_configured_key(self):
        old_value = os.environ.pop("SEEDANCE_API_KEY", None)
        try:
            with self.assertRaises(PermissionError):
                self.runtime.run(
                    "video-caption-repurpose",
                    "seedance",
                    "generate_video",
                    {
                        "prompt": "short product video",
                        "duration_seconds": 8,
                        "aspect_ratio": "9:16",
                        "usage_rights": "commercial_safe_generated_asset",
                    },
                    dry_run=False,
                )
        finally:
            if old_value is not None:
                os.environ["SEEDANCE_API_KEY"] = old_value

    def test_configured_key_still_returns_call_plan_until_live_adapter_enabled(self):
        old_value = os.environ.get("SEEDANCE_API_KEY")
        os.environ["SEEDANCE_API_KEY"] = "test-key"
        try:
            trace = self.runtime.run(
                "video-caption-repurpose",
                "seedance",
                "generate_video",
                {
                    "prompt": "short product video",
                    "duration_seconds": 8,
                    "aspect_ratio": "9:16",
                    "usage_rights": "commercial_safe_generated_asset",
                },
                dry_run=False,
            )
        finally:
            if old_value is None:
                os.environ.pop("SEEDANCE_API_KEY", None)
            else:
                os.environ["SEEDANCE_API_KEY"] = old_value

        self.assertEqual(trace.status, "planned")
        self.assertTrue(trace.call_plan["credential_configured"])
        self.assertFalse(trace.call_plan["live_call_allowed"])
        self.assertEqual(trace.call_plan["live_call_status"], "not_implemented")

    def test_provider_action_requires_registered_action_and_request_fields(self):
        with self.assertRaisesRegex(ValueError, "missing request fields"):
            self.runtime.run(
                "video-caption-repurpose",
                "seedance",
                "generate_video",
                {"prompt": "short product video"},
                dry_run=True,
            )

        with self.assertRaisesRegex(ValueError, "not supported"):
            self.runtime.run(
                "video-caption-repurpose",
                "seedance",
                "publish_video",
                {"prompt": "short product video"},
                dry_run=True,
            )

    def test_rejects_provider_not_allowed_for_service(self):
        with self.assertRaises(ValueError):
            self.runtime.run(
                "blog-article-writer",
                "seedance",
                "generate_video",
                {"prompt": "not allowed"},
                dry_run=True,
            )

    def test_every_provider_has_adapter_scaffold(self):
        for provider_id in self.catalog.providers:
            adapter = adapter_for(provider_id)
            self.assertEqual(adapter.provider_id, provider_id)
            self.assertTrue(adapter.actions)
            self.assertTrue(adapter.scopes)
            self.assertTrue(adapter.artifact_types)


if __name__ == "__main__":
    unittest.main()
