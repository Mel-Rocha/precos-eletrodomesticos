import requests
from bs4 import BeautifulSoup
import re


def scrape_product_price(url):
    # Realiza o request para a URL
    response = requests.get(url)

    # Verifica se a requisição foi bem-sucedida
    if response.status_code != 200:
        raise Exception("URL inválida ou não encontrada")

    # Parseia o conteúdo HTML
    soup = BeautifulSoup(response.content, 'html.parser')

    # Encontra todos os elementos que contêm "$"
    elementos_com_dollar = soup.find_all(text=lambda text: text and '$' in text)

    # Para cada elemento encontrado, extrai o valor
    for elemento in elementos_com_dollar:
        valor = elemento.split('$')[-1].strip()
        print("Valor encontrado (do BeautifulSoup):", valor)

    # Encontra todos os elementos que contêm a chave "Value"
    pattern = r'"Value"\s*:\s*([\d.]+)'
    matches = re.findall(pattern, response.text)

    # Se houver correspondências, extrai o valor encontrado
    if matches:
        valor_encontrado = matches[0]
        print("Valor encontrado (da expressão regular):", valor_encontrado)
    else:
        print("Nenhum valor correspondente encontrado.")


# Teste da função
url = "https://www.ikesaki.com.br/coloracao-igora-royal-7-00-louro-medio-natural-extra-60g/p"
scrape_product_price(url)
