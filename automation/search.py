import time

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys


def search_product_on_site(site_url, product):
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    driver.get(site_url)
    time.sleep(2)
    driver.find_element('xpath', '//*[@id="downshift-0-input"]').send_keys(product, Keys.ENTER)
    time.sleep(5)

    driver.quit()


product = "Coloração Igora Royal 8.77 Louro Claro Cobre Extra 60g"

sites = [
    {"url": "https://www.ikesaki.com.br/"},
    {"url": "https://www.mundodocabeleireiro.com.br/"}
]

for site in sites:
    search_product_on_site(site["url"], product)

