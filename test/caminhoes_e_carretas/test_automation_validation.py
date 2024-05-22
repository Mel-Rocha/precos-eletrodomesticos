import unittest

from automation.caminhoes_e_carretas.collect_url import CaminhoesECarretasAutomation


class TestCaminhoesECarretasAutomation(unittest.TestCase):

    def setUp(self):
        self.automation = CaminhoesECarretasAutomation()

    def test_automation_validation(self):
        page_number = 1
        num_div_elements = 21
        current_url_all = ["https://example.com/ad1", "https://example.com/ad2", "https://example.com/ad3"]
        old_len = 1

        result = self.automation.automation_validation(page_number, num_div_elements, current_url_all, old_len)

        self.assertIsInstance(result, dict)

        self.assertEqual(result['page_number'], page_number)
        self.assertEqual(result['ads_found'], num_div_elements)
        self.assertEqual(result['extracted_urls'], len(current_url_all) - old_len)

    def test_automation_validation_no_urls_extracted(self):
        page_number = 2
        num_div_elements = 0
        current_url_all = []
        old_len = 0

        result = self.automation.automation_validation(page_number, num_div_elements, current_url_all, old_len)

        self.assertEqual(result['page_number'], page_number)
        self.assertEqual(result['ads_found'], num_div_elements)
        self.assertEqual(result['extracted_urls'], len(current_url_all) - old_len)


if __name__ == '__main__':
    unittest.main()
