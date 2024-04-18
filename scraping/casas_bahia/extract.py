import requests
from bs4 import BeautifulSoup


def scrape_product_description(url, selector):
    # Realiza o request para a URL
    response = requests.get(url)
    # Verifica se a requisição foi bem-sucedida
    if response.status_code != 200:
        raise Exception("URL inválida ou não encontrada")

    # Parseia o conteúdo HTML
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extrai a descrição do produto usando o seletor CSS fornecido
    description_element = soup.select_one(selector)
    description = description_element.text.strip() if description_element else "Descrição não encontrada"

    print(description)
    return {"description": description}

url = 'https://www.casasbahia.com.br/geladeira-brastemp-french-door-bro85ak-frost-free-com-tecnologia-inverter-turbo-freezer-e-design-premium-inox-554-l/p/55054274?utm_source=gp_branding&utm_medium=cpc&utm_campaign=gg_brd_inst_cb_exata'
selector = '#__next > div > div:nth-child(2) > div.dsvia-flex.css-1jkjkxm > div.dsvia-box.css-p10hlm > h1'


print(scrape_product_description(url, selector))