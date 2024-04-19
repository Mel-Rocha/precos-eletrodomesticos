import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

def scrape_product_info(url):
    # Realiza o request para a URL
    response = requests.get(url)
    # Verifica se a requisição foi bem-sucedida
    if response.status_code != 200:
        raise Exception("URL inválida ou não encontrada")

    # Parseia o conteúdo HTML
    soup = BeautifulSoup(response.content, 'html.parser')

    # Encontra o título do produto
    product_element = soup.find('h1')
    product = product_element.text.strip() if product_element else None

    return product

url = 'https://www.ikesaki.com.br/coloracao-igora-royal-7-00-louro-medio-natural-extra-60g/p'

product_info_soup = scrape_product_info(url)
print("Produto (BeautifulSoup):", product_info_soup)

