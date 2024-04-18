import requests
from bs4 import BeautifulSoup

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

    # Encontra o elemento que contém o valor em reais
    reais_element = soup.find('span', class_='vtex-product-price-1-x-currencyInteger')
    reais = reais_element.text.strip() if reais_element else None

    # Encontra o elemento que contém os centavos
    centavos_element = soup.find('span', class_='vtex-product-price-1-x-currencyFraction')
    centavos = centavos_element.text.strip() if centavos_element else None

    # Concatena o valor em reais e os centavos, se ambos forem encontrados
    price = f"{reais},{centavos}" if reais and centavos else None

    # Retorna um dicionário com as chaves "product" e "price"
    return {"product": product, "price": price}

url = 'https://www.ikesaki.com.br/coloracao-igora-royal-8-77-louro-claro-cobre-extra-60g-76-37/p'
product_info = scrape_product_info(url)
print(product_info)




