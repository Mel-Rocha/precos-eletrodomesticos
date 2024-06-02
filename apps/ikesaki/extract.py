import logging
from datetime import datetime

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from tenacity import retry, stop_after_attempt

from apps.core.base_automation import CoreAutomation

logging.basicConfig(level=logging.INFO)


class IkesakiExtract(CoreAutomation):
    """
    Objetivo: Com base na lista de URLs especificas de cada anúncio, fazer a extração das informações relevantes.

    Obrigatório Fornecer: Lista de URLs.

    Retorno: tupla contendo:
        1. all_ltems_extract: Lista de dicionários com as informações extraídas de cada anúncio.
        2. extract_failure_analysis: Lista comtendo o nome dos métodos que falharam na extração.
        3. not_price: Lista de URLs dos anúncios que não têm preço.
    """

    def __init__(self, all_urls):
        super().__init__()
        self.all_urls = all_urls
        self.current_url = None
        self.fail_offer = {}
        self.extract_failure_analysis = []

    @retry(stop=stop_after_attempt(3))
    def fetch_page(self, url):
        self.driver.get(url)
        html_content = self.driver.page_source
        self.soup = BeautifulSoup(html_content, 'html.parser')
        self.fail_offer = {url: []}

    def product_extract(self):
        product_element = self.soup.find('h1')
        product = product_element.text.strip() if product_element else None
        return product

    def price_extract(self):
        try:
            price_integer_element = self.driver.find_element(By.XPATH,
                                                             '/html/body/div[2]/div/div[1]/div/div/div/div[2]/div/div[3]/div/section/div/div[2]/div/div[5]/div/div/div/div/div[3]/div/div[1]/div/div/div[2]/div/div[1]/div/div[2]/span/span/span/span[3]')
            price_fraction_element = self.driver.find_element(By.XPATH,
                                                              '/html/body/div[2]/div/div[1]/div/div/div/div[2]/div/div[3]/div/section/div/div[2]/div/div[5]/div/div/div/div/div[3]/div/div[1]/div/div/div[2]/div/div[1]/div/div[2]/span/span/span/span[5]')
            price_integer = price_integer_element.text
            price_fraction = price_fraction_element.text
            if price_integer.isdigit() and price_fraction.isdigit():
                price = float(f'{price_integer}.{price_fraction}')
                return price
        except Exception as e:
            print(f"An error occurred: {e}")
        return None

    def url_extract(self):
        return self.current_url

    @staticmethod
    def crawling_date_extract():
        now = datetime.now()
        return now.strftime("%Y-%m-%d %H:%M:%S")

    def extract(self):
        all_ltems_extract = []
        not_price = []
        for url in self.all_urls:
            self.current_url = url
            self.fetch_page(url)
            price = self.price_extract()
            if price is None:
                not_price.append(url)
                continue
            item = {
                'price': price,
                'product': self.product_extract(),
                'url': self.url_extract(),
                'crawling_date': IkesakiExtract.crawling_date_extract(),
            }
            all_ltems_extract.append(item)

            if self.fail_offer[url]:
                self.extract_failure_analysis.append(self.fail_offer)

        self.driver.quit()

        logging.info(f"Anúncios Extraídos: {all_ltems_extract}")
        logging.info(f"Falha na Extração: {self.extract_failure_analysis}")
        logging.info(f"Anúncios sem Preço: {not_price}")

        return all_ltems_extract, self.extract_failure_analysis, not_price


if __name__ == "__main__":
    urls = [
        "https://www.ikesaki.com.br/coloracao-keune-so-pure-color-60ml-4-castanho-medio/p",
    ]
    e = IkesakiExtract(urls)
    extract = e.extract()
