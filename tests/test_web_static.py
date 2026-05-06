import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class WebStaticTest(unittest.TestCase):
    def test_alpha_ui_contains_required_buyer_flow_regions(self):
        html = (ROOT / "web" / "index.html").read_text(encoding="utf-8")
        for required in [
            'aria-label="Service catalog"',
            'aria-label="Selected service workroom"',
            'id="serviceRows"',
            'id="briefFields"',
            'id="checkoutBtn"',
            "Provider Dry-Run Status",
            "Price & SLA Summary",
        ]:
            self.assertIn(required, html)

    def test_alpha_ui_embeds_20_mvp_services(self):
        js = (ROOT / "web" / "app.js").read_text(encoding="utf-8")
        slugs = set(re.findall(r'slug: "([^"]+)"', js))
        self.assertEqual(len(slugs), 20)
        self.assertIn("video-caption-repurpose", slugs)
        self.assertIn("product-image-editing", slugs)


if __name__ == "__main__":
    unittest.main()

