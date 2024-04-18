import requests
from bs4 import BeautifulSoup

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
        print("Valor encontrado:", valor)

url = 'https://www.ikesaki.com.br/coloracao-igora-royal-8-77-louro-claro-cobre-extra-60g-76-37/p'
scrape_product_price(url)


