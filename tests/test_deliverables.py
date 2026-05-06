import json
import tempfile
import unittest
from pathlib import Path

from agent_fiverr.deliverables import DeliverablePackager


class DeliverablePackagerTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.packager = DeliverablePackager(self.root)

    def tearDown(self):
        self.tmp.cleanup()

    def test_packages_markdown_document_with_manifest(self):
        packaged = self.packager.package(
            order_id="order-1",
            surface="document",
            title="SEO Audit",
            content={"Summary": "Ready", "Findings": "Fix titles"},
            metadata={"version": 1},
        )
        self.assertEqual(packaged.mime_type, "text/markdown")
        self.assertIn("SEO Audit", (self.root / packaged.path).read_text(encoding="utf-8"))
        manifest = json.loads((self.root / packaged.manifest_path).read_text(encoding="utf-8"))
        self.assertEqual(manifest["metadata"]["version"], 1)

    def test_packages_csv_table(self):
        packaged = self.packager.package(
            order_id="order-1",
            surface="table",
            title="Cleaned Contacts",
            content=[
                {"email": "a@example.com", "name": "A"},
                {"email": "b@example.com", "name": "B"},
            ],
        )
        content = (self.root / packaged.path).read_text(encoding="utf-8")
        self.assertIn("email,name", content)
        self.assertIn("a@example.com,A", content)

    def test_packages_html_widget_and_rejects_invalid_surface_content(self):
        packaged = self.packager.package(
            order_id="order-1",
            surface="widget",
            title="Dashboard",
            content={"metric": "Revenue", "value": "$10k"},
        )
        html = (self.root / packaged.path).read_text(encoding="utf-8")
        self.assertIn("data-agent-fiverr-widget", html)
        with self.assertRaises(TypeError):
            self.packager.package(order_id="order-1", surface="table", title="Bad", content=[])


if __name__ == "__main__":
    unittest.main()
