import unittest
from pathlib import Path

from agent_fiverr.catalog import Catalog


ROOT = Path(__file__).resolve().parents[1]


class CatalogTest(unittest.TestCase):
    def test_loads_20_services(self):
        catalog = Catalog(ROOT)
        self.assertEqual(len(catalog.services), 20)

    def test_validates_required_brief_fields(self):
        catalog = Catalog(ROOT)
        missing = catalog.validate_brief("seo-geo-audit", {"website_url": "https://example.com"})
        self.assertIn("target_market", missing)
        self.assertIn("business_goal", missing)

    def test_media_services_reference_expected_providers(self):
        catalog = Catalog(ROOT)
        video = catalog.get_service("video-caption-repurpose")
        self.assertIn("seedance", video.api_providers)
        self.assertIn("elevenlabs", video.api_providers)
        image = catalog.get_service("product-image-editing")
        self.assertIn("banana", image.api_providers)
        self.assertIn("gpt_image_2", image.api_providers)


if __name__ == "__main__":
    unittest.main()

