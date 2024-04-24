import unittest

from automation.product.search import AutomationSearchProduct


class AutomationSearchProductTest(unittest.TestCase):
    def setUp(self):
        self.automation = AutomationSearchProduct()
        self.generic_product = "Cabelo"
        self.site_domain = "https://www.ikesaki.com.br/"

    def test_search_product_all(self):
        urls = self.automation.search_product_all(self.generic_product, self.site_domain)
        self.assertIsInstance(urls, list, "The result should be a list")
        self.assertTrue(all(isinstance(url, str) for url in urls), "All elements in the list should be strings")


if __name__ == "__main__":
    unittest.main()
