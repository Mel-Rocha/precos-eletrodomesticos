import logging
from datetime import datetime

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

from automation.core_automation.base_automation import CoreAutomation

logging.basicConfig(level=logging.INFO)


class BackhoeExtract(CoreAutomation):
    """
    Objetivo: Com base na lista de URLs especificadas, fazer a extração das informações relevantes.

    Obrigatório Fornecer: Lista de URLs.

    Retorno: Lista de dicionários com valores obtidos de cada produto específico.
    """

    def __init__(self, backhoe_urls):
        super().__init__()
        self.backhoe_urls = backhoe_urls
        self.current_url = None

    def fetch_page(self, url):
        self.driver.get(url)
        html_content = self.driver.page_source
        self.soup = BeautifulSoup(html_content, 'html.parser')
        self.div_information = self.driver.find_element(By.XPATH, '//*[@id="tab1"]/div/div/div[1]')

    def fabricator_extract(self):
        fabricator_element = self.soup.select_one('p:contains("Marca") > strong')
        return fabricator_element.text.strip() if fabricator_element else None

    def model_extract(self):
        model_element = self.soup.select_one('p:contains("Modelo") > strong')
        return model_element.text.strip() if model_element else None

    def year_extract(self):
        year_element = self.soup.select_one('p:contains("Ano") > strong')
        return year_element.text.strip() if year_element else None

    def price_extract(self):
        price_element = self.soup.select_one('p:contains("Preço") > strong')
        return price_element.text.strip() if price_element else None

    def worked_hours_extract(self):
        worked_hours_element = self.soup.select_one('p:contains("Horas") > strong')
        return worked_hours_element.text.strip() if worked_hours_element else None

    def url_extract(self):
        return self.current_url

    @staticmethod
    def crawling_date_extract():
        now = datetime.now()
        return now.strftime("%Y-%m-%d %H:%M:%S")

    def extract(self):
        backhoe_list = []
        for url in self.backhoe_urls:
            self.current_url = url
            self.fetch_page(url)
            backhoe = {
                'fabricator': self.fabricator_extract(),
                'model': self.model_extract(),
                'year': self.year_extract(),
                'price': self.price_extract(),
                'worked_hours': self.worked_hours_extract(),
                'url': self.url_extract(),
                'crawling_date': BackhoeExtract.crawling_date_extract(),
            }
            backhoe_list.append(backhoe)

        self.driver.quit()
        return backhoe_list

