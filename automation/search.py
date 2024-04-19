import time

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys

# Configuração do Selenium
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)



# Produto a ser buscado
product = "Coloração Igora Royal 8.77 Louro Claro Cobre Extra 60g"

# Sites para busca
sites = [
    {"url": "https://www.ikesaki.com.br/", "input_xpath": '//*[@id="downshift-0-input"]'},
    # Adicione outros sites conforme necessário
]

for site in sites:
    # Abrir o site
    driver.get(site["url"])
    time.sleep(2)  # Espera para garantir que a página seja carregada completamente

    driver.find_element('xpath', '//*[@id="downshift-0-input"]').send_keys(product, Keys.ENTER)
    time.sleep(5)


    driver.quit()
