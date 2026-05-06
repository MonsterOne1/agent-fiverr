import tempfile
import unittest
from pathlib import Path

from agent_fiverr.catalog import Catalog
from agent_fiverr.order import OrderRuntime


ROOT = Path(__file__).resolve().parents[1]


class OrderRuntimeTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        for dirname in ["data", "services"]:
            source = ROOT / dirname
            target = self.root / dirname
            target.symlink_to(source, target_is_directory=True)
        self.catalog = Catalog(self.root)
        self.runtime = OrderRuntime(self.root, self.catalog)

    def tearDown(self):
        self.tmp.cleanup()

    def complete_seo_brief(self):
        return {
            "website_url": "https://example.com",
            "target_market": "US",
            "target_keywords": "ai notes",
            "competitors": "competitor a",
            "cms": "Webflow",
            "business_goal": "increase demos",
        }

    def test_create_order_persists_audit(self):
        order = self.runtime.create_order("seo-geo-audit", self.complete_seo_brief())
        loaded = self.runtime.load(order.order_id)
        self.assertEqual(loaded.state, "intake")
        self.assertEqual(loaded.missing_brief_fields, [])
        self.assertEqual(loaded.audit[0].kind, "order_created")

    def test_lifecycle_requires_next_state(self):
        order = self.runtime.create_order("seo-geo-audit", self.complete_seo_brief())
        with self.assertRaises(ValueError):
            self.runtime.transition(order, "plan")
        self.runtime.transition(order, "scope_check")
        self.assertEqual(order.state, "scope_check")

    def test_blocks_side_effect_provider_without_authorization(self):
        order = self.runtime.create_order("website-bug-fix", {
            "repo_url": "https://github.com/example/repo",
            "bug_description": "Button does not submit",
            "repro_steps": "Open page and click submit",
            "expected_behavior": "Form submits",
            "environment": "preview",
            "access_scope": "read-only",
        })
        with self.assertRaises(PermissionError):
            self.runtime.require_provider_action(order, "github", "push_branch")
        loaded = self.runtime.load(order.order_id)
        self.assertEqual(loaded.audit[-1].kind, "authorization_blocked")

    def test_allows_side_effect_after_authorization(self):
        order = self.runtime.create_order("website-bug-fix", {
            "repo_url": "https://github.com/example/repo",
            "bug_description": "Button does not submit",
            "repro_steps": "Open page and click submit",
            "expected_behavior": "Form submits",
            "environment": "preview",
            "access_scope": "branch write",
        })
        self.runtime.authorize(order, "github:push_branch")
        self.runtime.require_provider_action(order, "github", "push_branch")
        self.assertEqual(order.audit[-1].kind, "provider_action_allowed")

    def test_blocks_low_quality_deliverable(self):
        order = self.runtime.create_order("seo-geo-audit", self.complete_seo_brief())
        with self.assertRaises(ValueError):
            self.runtime.add_deliverable(order, {"summary": "thin"}, qa_score=3, qa_notes=["needs sources"])

    def test_versions_approved_deliverables(self):
        order = self.runtime.create_order("seo-geo-audit", self.complete_seo_brief())
        self.runtime.add_deliverable(order, {"summary": "ok"}, qa_score=4, qa_notes=["checked"])
        self.runtime.add_deliverable(order, {"summary": "better"}, qa_score=5, qa_notes=["checked"])
        self.assertEqual([item.version for item in order.deliverables], [1, 2])

    def test_revision_scope_detection(self):
        order = self.runtime.create_order("seo-geo-audit", self.complete_seo_brief())
        in_scope = self.runtime.request_revision(order, "Change target keyword", ["target_keywords"])
        out_scope = self.runtime.request_revision(order, "Also redesign the website", ["website_redesign"])
        self.assertTrue(in_scope.in_scope)
        self.assertFalse(out_scope.in_scope)


if __name__ == "__main__":
    unittest.main()

