import re
import time
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup


class ExtractProductPriceStore:
    """
    Objective:
    extract relevant product information (such as name, price and store name)
    through web scraping based on its URL

    Parameters:
    url = "https://www.ikesaki.com.br/progressiva-borabella-nao-chore-mais-1000g/p"
    """
    def __init__(self, url):
        self.url = url
        self.response = self._get_response()
        self.soup = BeautifulSoup(self.response.content, 'html.parser')

    def _get_response(self):
        headers = {'User-Agent': 'My User Agent 1.0'}
        for i in range(10):
            try:
                response = requests.get(self.url, headers=headers)
                response.raise_for_status()
            except requests.exceptions.HTTPError as err:
                if response.status_code == 429:
                    print("Too many requests. Waiting and trying again.")
                    time.sleep(2 ** i)
                    continue
                else:
                    raise Exception(f"URL inválida ou não encontrada. "
                                    f"URL: {self.url} "
                                    f"STATUS CODE: {response.status_code}") from err
            break
        return response

    def extract_product(self):
        product_element = self.soup.find('h1')
        product = product_element.text.strip() if product_element else None
        return product

    def extract_price(self):
        price_from_regex = None
        pattern = r'"Value"\s*:\s*([\d.]+)'
        matches = re.findall(pattern, self.response.text)

        if matches:
            price_from_regex = matches[0]
        else:
            price_from_regex = "Nenhum valor correspondente encontrado."

        return price_from_regex

    def extract_store(self):
        parsed_url = urlparse(self.url)
        domain = parsed_url.netloc
        store = domain.split(".")[1]
        return store


