import unittest

from agent_fiverr.long_tail import generate_long_tail_services, validate_long_tail_services


class LongTailCatalogTest(unittest.TestCase):
    def test_generates_500_plus_service_specs_and_100_saleable_candidates(self):
        services = generate_long_tail_services()
        self.assertGreaterEqual(len(services), 500)
        saleable = [service for service in services if service["saleable_candidate"]]
        self.assertGreaterEqual(len(saleable), 100)

    def test_every_long_tail_service_has_minimum_eval_pack(self):
        services = generate_long_tail_services()
        result = validate_long_tail_services(services)
        self.assertTrue(result.passed)
        self.assertEqual(result.failures, ())


if __name__ == "__main__":
    unittest.main()

