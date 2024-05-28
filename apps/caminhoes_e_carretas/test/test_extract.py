import unittest
from unittest.mock import patch, MagicMock

from apps.caminhoes_e_carretas.extract import BackhoeExtract


class TestBackhoeExtract(unittest.TestCase):
    @patch('apps.caminhoes_e_carretas.extract.BeautifulSoup')
    @patch('apps.caminhoes_e_carretas.extract.CoreAutomation')
    def setUp(self, mock_CoreAutomation, mock_BeautifulSoup):
        self.mock_CoreAutomation = mock_CoreAutomation
        self.mock_BeautifulSoup = mock_BeautifulSoup
        self.urls = [
            "https://www.caminhoesecarretas.com.br/veiculo/maravilha/sc/retro-escavadeira/jcb/4cx11/2009/tracao-4x4"
            "/cabi"]
        self.extractor = BackhoeExtract(self.urls)

    def test_price_extract(self):
        mock_soup = MagicMock()
        self.extractor.soup = mock_soup
        self.extractor.current_url = self.urls[0]
        self.extractor.fail_backhoe[self.extractor.current_url] = []

        test_cases = [
            ('R$ 10000,00', 1000000),  # string and digits
            ('R$ 10000,00 @ Test', 1000000),  # price and other special characters
            ('(Á consultar)', None)  # string without digits
        ]

        for text, expected in test_cases:
            with self.subTest(text=text):
                mock_soup.select_one.return_value = MagicMock(text=text)
                result = self.extractor.price_extract()
                self.assertEqual(result, expected)
                if expected is None:
                    self.assertIn('price_element', self.extractor.fail_backhoe[self.extractor.current_url])


if __name__ == '__main__':
    unittest.main()
