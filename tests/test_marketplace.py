import tempfile
import unittest
from pathlib import Path

from agent_fiverr.catalog import Catalog
from agent_fiverr.marketplace import Marketplace
from agent_fiverr.order import OrderRuntime


ROOT = Path(__file__).resolve().parents[1]


class MarketplaceTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        for dirname in ["data", "services"]:
            (self.root / dirname).symlink_to(ROOT / dirname, target_is_directory=True)
        self.catalog = Catalog(self.root)
        self.marketplace = Marketplace(self.catalog, OrderRuntime(self.root, self.catalog))

    def tearDown(self):
        self.tmp.cleanup()

    def test_discovers_services_by_category(self):
        services = self.marketplace.discover(category="Data")
        slugs = {service.slug for service in services}
        self.assertIn("data-cleaning-formatting", slugs)
        self.assertIn("dashboard-prototype", slugs)

    def test_rejects_quote_when_brief_is_missing_required_fields(self):
        quote = self.marketplace.quote("seo-geo-audit", {"website_url": "https://example.com"})
        self.assertFalse(quote.ready)
        self.assertIn("target_market", quote.missing_fields)

    def test_creates_ready_quote_with_package_price_and_sla(self):
        quote = self.marketplace.quote("data-cleaning-formatting", {
            "dataset_file": "contacts.csv",
            "target_schema": "email,name",
            "dedupe_rules": "email",
            "missing_value_rules": "blank",
            "output_format": "csv",
        }, package="standard")
        self.assertTrue(quote.ready)
        self.assertEqual(quote.price_usd, 150)
        self.assertEqual(quote.sla_hours, 24)

    def test_accepting_quote_creates_order_and_escrow_hold(self):
        quote = self.marketplace.quote("data-cleaning-formatting", {
            "dataset_file": "contacts.csv",
            "target_schema": "email,name",
            "dedupe_rules": "email",
            "missing_value_rules": "blank",
            "output_format": "csv",
        })
        checkout = self.marketplace.accept_quote(quote, buyer_id="buyer-1")
        self.assertEqual(checkout.escrow_status, "held")
        self.assertEqual(checkout.escrow_provider, "mock")
        self.assertTrue(checkout.escrow_hold_id)
        loaded = self.marketplace.order_runtime.load(checkout.order_id)
        self.assertEqual(loaded.service_slug, "data-cleaning-formatting")

    def test_accepting_quote_can_use_stripe_connect_scaffold(self):
        quote = self.marketplace.quote("data-cleaning-formatting", {
            "dataset_file": "contacts.csv",
            "target_schema": "email,name",
            "dedupe_rules": "email",
            "missing_value_rules": "blank",
            "output_format": "csv",
        })
        checkout = self.marketplace.accept_quote(
            quote,
            buyer_id="buyer-1",
            escrow_provider="stripe_connect",
            dry_run_payment=True,
        )
        self.assertEqual(checkout.escrow_provider, "stripe_connect")
        self.assertEqual(checkout.escrow_status, "planned")


if __name__ == "__main__":
    unittest.main()
