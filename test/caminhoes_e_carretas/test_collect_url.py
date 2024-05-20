import logging
import unittest
from unittest.mock import MagicMock, patch

from selenium.common.exceptions import TimeoutException, NoSuchElementException

from automation.caminhoes_e_carretas.collect_url import CaminhoesECarretasAutomation

logging.basicConfig(level=logging.INFO)


class TestCaminhoesECarretasAutomation(unittest.TestCase):

    def setUp(self):
        self.automation = CaminhoesECarretasAutomation()

    @patch('automation.caminhoes_e_carretas.collect_url.CaminhoesECarretasAutomation.access_url')
    def test_access_url(self, mock_access_url):
        # Configuração do mock
        mock_access_url.return_value = None

        # Chama o método e verifica o retorno
        result = self.automation.access_url()
        self.assertIsNone(result)

    @patch('selenium.webdriver.Chrome')
    @patch('selenium.webdriver.support.ui.WebDriverWait.until')
    def test_backhoe_url_all(self, mock_wait_until, mock_webdriver):
        # Configuração do mock
        self.automation.driver = MagicMock()
        mock_webdriver.return_value = self.automation.driver
        mock_wait_until.return_value = True

        # Simulação de HTMLs de páginas com anúncios
        html_content_with_ads = '''
            <div class="productList">
                <div class="item-veiculo">
                    <a id="ContentPlaceHolder1_lvVeiculo_lnkVeiculo_0">
                        <img src="img1.jpg"/>
                    </a>
                </div>
                <div class="item-veiculo">
                    <a id="ContentPlaceHolder1_lvVeiculo_lnkVeiculo_1">
                        <img src="img2.jpg"/>
                    </a>
                </div>
            </div>
            '''
        html_content_no_ads = '<div class="productList"></div>'

        # Contador de página para limitar a paginação
        self.page_counter = 0
        max_pages = 5  # Limite de páginas para o teste

        # Simulação de driver.page_source retornando diferentes HTMLs
        def get_page_source_side_effect():
            if self.page_counter < max_pages:
                return html_content_with_ads
            else:
                return html_content_no_ads

        def get_current_url_side_effect():
            return f"https://www.caminhoesecarretas.com.br/venda/retro%20escavadeira/24?page={self.page_counter}"

        def increment_page_counter(url):
            self.page_counter += 1

        self.automation.driver.page_source = MagicMock(side_effect=get_page_source_side_effect)
        self.automation.driver.current_url = MagicMock(side_effect=get_current_url_side_effect)
        self.automation.driver.get.side_effect = increment_page_counter
        self.automation.driver.find_element.side_effect = lambda *args, **kwargs: MagicMock()

        # Adicionar logging para debug
        import logging
        logging.basicConfig(level=logging.INFO)

        # Chama o método e verifica o retorno
        result = self.automation.backhoe_url_all()
        logging.info(f"URLs extraídas: {result[0]}")
        logging.info(f"Métricas: {result[1]}")
        logging.info(f"Falhas: {result[2]}")

        self.assertEqual(len(result[0]), 10)  # Deve ter dez URLs extraídas (2 por página)
        self.assertEqual(len(result[1]), 5)  # Deve ter métricas para cinco páginas
        for i in range(5):
            self.assertEqual(result[1][i]['page_number'], i)
            self.assertEqual(result[1][i]['ads_found'], 2)
            self.assertEqual(result[1][i]['urls_extracted'], 2)
        self.assertEqual(result[2], [])  # Nenhuma falha deve ocorrer

    @patch('selenium.webdriver.support.ui.WebDriverWait.until')
    @patch('selenium.webdriver.Chrome')
    def test_backhoe_url_all_with_failures(self, mock_webdriver, mock_wait_until):
        # Configuração do mock
        self.automation.driver = MagicMock()
        mock_webdriver.return_value = self.automation.driver
        mock_wait_until.side_effect = TimeoutException

        # Simulação de um HTML de página com anúncios
        html_content = '''
            <div class="productList">
                <div class="item-veiculo">
                    <a id="ContentPlaceHolder1_lvVeiculo_lnkVeiculo_0">
                        <img src="img1.jpg"/>
                    </a>
                </div>
            </div>
            '''

        self.automation.driver.page_source = html_content
        self.automation.driver.find_element.side_effect = NoSuchElementException

        # Contador de página para limitar a paginação
        self.page_counter = 0
        max_pages = 5  # Limite de páginas para o teste

        def get_page_source_side_effect():
            if self.page_counter < max_pages:
                return html_content
            else:
                return '<div class="productList"></div>'

        def get_current_url_side_effect():
            return f"https://www.caminhoesecarretas.com.br/venda/retro%20escavadeira/24?page={self.page_counter}"

        def increment_page_counter(url):
            self.page_counter += 1

        self.automation.driver.page_source = MagicMock(side_effect=get_page_source_side_effect)
        self.automation.driver.current_url = MagicMock(side_effect=get_current_url_side_effect)
        self.automation.driver.get.side_effect = increment_page_counter

        # Chama o método e verifica o retorno
        result = self.automation.backhoe_url_all()
        logging.info(f"URLs extraídas: {result[0]}")
        logging.info(f"Métricas: {result[1]}")
        logging.info(f"Falhas: {result[2]}")

        self.assertEqual(result[0], [])  # Nenhuma URL deve ser extraída
        self.assertEqual(len(result[1]), 5)  # Deve ter métricas para cinco páginas
        for i in range(5):
            self.assertEqual(result[1][i]['page_number'], i)
            self.assertEqual(result[1][i]['ads_found'], 1)
            self.assertEqual(result[1][i]['urls_extracted'], 0)
        self.assertEqual(len(result[2]), 5)  # Deve haver cinco falhas


if __name__ == '__main__':
    unittest.main()