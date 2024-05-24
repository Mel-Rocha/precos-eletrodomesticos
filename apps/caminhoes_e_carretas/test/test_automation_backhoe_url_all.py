import unittest
from unittest.mock import MagicMock, patch

from apps.caminhoes_e_carretas.automation import CaminhoesECarretasAutomation


class TestBackhoeUrlAll(unittest.TestCase):

    @patch('automation.caminhoes_e_carretas.collect_url.BeautifulSoup')
    @patch('automation.caminhoes_e_carretas.collect_url.WebDriverWait')
    @patch('automation.caminhoes_e_carretas.collect_url.time.sleep', return_value=None)
    def test_backhoe_url_all(self, mock_sleep, mock_webdriverwait, mock_beautifulsoup):
        mock_driver = MagicMock()
        mock_driver.page_source = '<html></html>'

        automation = CaminhoesECarretasAutomation()
        automation.driver = mock_driver

        mock_soup_instance = MagicMock()
        mock_beautifulsoup.return_value = mock_soup_instance

        mock_all_product = MagicMock()
        mock_soup_instance.find.return_value = mock_all_product

        mock_div_elements = [MagicMock(), MagicMock()]
        mock_all_product.find_all.return_value = mock_div_elements

        mock_wait_instance = MagicMock()
        mock_webdriverwait.return_value.until.return_value = mock_wait_instance

        def side_effect_script(script, element):
            new_url = f"https://example.com/vehicle/{len(automation.current_url_all)}"
            mock_driver.current_url = new_url
            automation.current_url_all.append(new_url)

            if len(automation.current_url_all) >= 3:
                raise Exception("Reached 3 URLs")

        mock_driver.execute_script.side_effect = side_effect_script

        result = automation.backhoe_url_all()

        current_url_all, metrics, automation_failure_analysis = result

        self.assertIsInstance(current_url_all, list, "current_url_all should be a list")
        self.assertIsInstance(metrics, list, "metrics should be a list")
        self.assertTrue(all(isinstance(item, dict) for item in metrics), "Each item in metrics should be a dict")
        self.assertIsInstance(automation_failure_analysis, list, "automation_failure_analysis should be a list")


if __name__ == '__main__':
    unittest.main()