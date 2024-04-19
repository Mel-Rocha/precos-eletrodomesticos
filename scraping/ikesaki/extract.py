import re

import requests
from bs4 import BeautifulSoup


class ExtractProductPrice:
    def __init__(self, url):
        self.url = url
        self.response = self._get_response()
        self.soup = BeautifulSoup(self.response.content, 'html.parser')

    def _get_response(self):
        response = requests.get(self.url)
        if response.status_code != 200:
            raise Exception("URL inválida ou não encontrada")
        return response

    def extract_product(self):
        product_element = self.soup.find('h1')
        product = product_element.text.strip() if product_element else None
        return product

    def extract_price(self):
        if self.response.status_code != 200:
            raise Exception("URL inválida ou não encontrada")

        price_from_regex = None
        pattern = r'"Value"\s*:\s*([\d.]+)'
        matches = re.findall(pattern, self.response.text)

        if matches:
            price_from_regex = matches[0]
        else:
            price_from_regex = "Nenhum valor correspondente encontrado."

        return price_from_regex

# Teste da classe
url = 'https://www.ikesaki.com.br/coloracao-igora-royal-8-77-louro-claro-cobre-extra-60g-76-37/p'
extractor = ExtractProductPrice(url)
product = extractor.extract_product()
price = extractor.extract_price()

result = {"product": product, "price": price}
print(result)

