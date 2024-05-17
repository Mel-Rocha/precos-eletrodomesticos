import logging

from bs4 import BeautifulSoup

from automation.core_automation.base_automation import CoreAutomation

logging.basicConfig(level=logging.INFO)


class BackhoeExtract(CoreAutomation):
    """
    Objetivo: Com base na url especifica fazer a extração das informações relevantes.

    Retorno: Dicionário com valores obtidos do produto específico.
    """

    def __init__(self, backhoe_url_specific):
        super().__init__()
        self.backhoe_url_specific = backhoe_url_specific
        self.driver.get(self.backhoe_url_specific)
        html_content = self.driver.page_source
        self.soup = BeautifulSoup(html_content, 'html.parser')

    def fabricator_extract(self):
        pass

    def model_extract(self):
        pass

    def year_extract(self):
        pass

    def price_extract(self):
        pass

    def worked_hours_extract(self):
        pass

    def crawling_date_extract(self):
        pass

    def url_extract(self):
        pass

    def extract(self):
        backhoe = {
            'fabricator': self.fabricator_extract(),
            'model': self.model_extract(),
            'year': self.year_extract(),
            'price': self.price_extract(),
            'worked_hours': self.worked_hours_extract(),
            'crawling_date': self.crawling_date_extract(),
            'url': self.url_extract(),
        }

        return backhoe


if __name__ == "__main__":
    e = BackhoeExtract(
        "https://www.caminhoesecarretas.com.br/veiculo/nova-andradina/ms/retro-escavadeira/case/580l/tk-tratores"
        "/1113197")
    extract = e.extract()
