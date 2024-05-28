import re
import logging
from datetime import datetime

from bs4 import BeautifulSoup
from tenacity import retry, stop_after_attempt

from apps.core.base_automation import CoreAutomation

logging.basicConfig(level=logging.INFO)


class BackhoeExtract(CoreAutomation):
    """
    Objetivo: Com base na lista de URLs especificas de cada anúncio, fazer a extração das informações relevantes.

    Obrigatório Fornecer: Lista de URLs.

    Retorno: tupla contendo:
        1. backhoe_list: Lista de dicionários com as informações extraídas de cada anúncio.
        2. extract_failure_analysis: Lista de análises de falhas de extração.
        3. not_price: Lista de URLs dos anúncios que não têm preço.
    """

    def __init__(self, backhoe_urls):
        super().__init__()
        self.backhoe_urls = backhoe_urls
        self.current_url = None
        self.fail_backhoe = {}
        self.extract_failure_analysis = []

    @retry(stop=stop_after_attempt(3))
    def fetch_page(self, url):
        self.driver.get(url)
        html_content = self.driver.page_source
        self.soup = BeautifulSoup(html_content, 'html.parser')
        self.fail_backhoe = {url: []}

    def clean_data(self, data):
        data = data.replace('\n', ' ').replace('\xa0', ' ').strip()
        cleaned_data = ' '.join(data.split())
        return cleaned_data

    def description_extract(self):
        description_element = self.soup.select_one('div.col-lg-4.col-md-4.col-sm-12.col-12')
        if description_element is None:
            self.fail_backhoe[self.current_url].append('description_extract')
            return None
        description = description_element.text
        cleaned_description = self.clean_data(description)
        if len(cleaned_description) >= 550:
            cleaned_description = cleaned_description[:550]
        return cleaned_description

    def fabricator_extract(self):
        fabricator_element = self.soup.select_one('p:contains("Marca") > strong')
        if fabricator_element is None:
            self.fail_backhoe[self.current_url].append('fabricator_extract')
        return fabricator_element.text.strip() if fabricator_element else None

    def model_extract(self):
        model_element = self.soup.select_one('p:contains("Modelo") > strong')
        if model_element is None:
            self.fail_backhoe[self.current_url].append('model_element')
        return model_element.text.strip() if model_element else None

    def year_extract(self):
        year_element = self.soup.select_one('p:contains("Ano") > strong')
        if year_element is None:
            self.fail_backhoe[self.current_url].append('year_element')
            return None
        year = year_element.text.strip()
        year_digits = "".join(re.findall(r'\d', year))
        if not year_digits:
            self.fail_backhoe[self.current_url].append('worked_hours_element')
            return None
        return int(year_digits)

    def price_extract(self):
        price_element = self.soup.select_one('p:contains("Preço") > strong')
        if price_element is None:
            self.fail_backhoe[self.current_url].append('price_element')
            return None
        price = price_element.text.strip()
        price_digits = "".join(re.findall(r'\d', price))
        if not price_digits:
            self.fail_backhoe[self.current_url].append('price_element')
            return None
        return int(price_digits)

    def worked_hours_extract(self):
        worked_hours_element = self.soup.select_one('p:contains("Horas") > strong')
        if worked_hours_element is None:
            self.fail_backhoe[self.current_url].append('worked_hours_element')
            return None
        worked_hours = worked_hours_element.text.strip()
        worked_hours_digits = "".join(re.findall(r'\d', worked_hours))
        if not worked_hours_digits:
            self.fail_backhoe[self.current_url].append('worked_hours_element')
            return None
        return int(worked_hours_digits)

    def url_extract(self):
        return self.current_url

    @staticmethod
    def crawling_date_extract():
        now = datetime.now()
        return now.strftime("%Y-%m-%d %H:%M:%S")

    def extract(self):
        backhoe_list = []
        not_price = []
        for url in self.backhoe_urls:
            self.current_url = url
            self.fetch_page(url)
            price = self.price_extract()
            if price is None:
                not_price.append(url)
                continue
            backhoe = {
                'fabricator': self.fabricator_extract(),
                'model': self.model_extract(),
                'year': self.year_extract(),
                'price': price,
                'worked_hours': self.worked_hours_extract(),
                'description': self.description_extract(),
                'url': self.url_extract(),
                'crawling_date': BackhoeExtract.crawling_date_extract(),
            }
            backhoe_list.append(backhoe)

            if self.fail_backhoe[url]:
                self.extract_failure_analysis.append(self.fail_backhoe)

        self.driver.quit()

        logging.info(f"Anúncios Extraídos: {backhoe_list}")
        logging.info(f"Falha na Extração: {self.extract_failure_analysis}")
        logging.info(f"Anúncios sem Preço: {not_price}")

        return backhoe_list, self.extract_failure_analysis, not_price


if __name__ == "__main__":
    urls = [
        "https://www.caminhoesecarretas.com.br/veiculo/maravilha/sc/retro-escavadeira/jcb/4cx11/2009/tracao-4x4/cabi"
        "ne-fechada/patrolao-maquinas/1181766",
        "https://www.caminhoesecarretas.com.br/veiculo/aruja/sp/retro-escavadeira/new-holland/b95b/2012/tracao-4x4/c"
        "abine-fechada/cattrucks/1118497",
        "https://www.caminhoesecarretas.com.br/veiculo/catanduva/sp/retro-escavadeira/jcb/4cx11/2021/tracao-4x4/cabine-"
        "fechada/manoel-tratores/1170789"
    ]
    e = BackhoeExtract(urls)
    extract = e.extract()
