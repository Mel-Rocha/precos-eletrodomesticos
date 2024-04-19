import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def search_product_on_site(site_url, product):
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    driver.get(site_url)
    time.sleep(2)
    search_box = driver.find_element('xpath', '//*[@id="downshift-0-input"]')
    search_box.send_keys(product, Keys.ENTER)
    time.sleep(5)

    html_content = driver.page_source

    soup = BeautifulSoup(html_content, 'html.parser')

    gallery_div = soup.find('div', {'id': 'gallery-layout-container'})
    if gallery_div:
        first_img = gallery_div.find('img')
        if first_img:
            img_element = driver.find_element('xpath', '//*[@id="gallery-layout-container"]/div/section/a/article'
                                                       '/div[1]/div[1]/div/div/img')

            img_element.click()

            time.sleep(3)

            if driver.current_url != site_url:
                print("Redirecionado para:", driver.current_url)
            else:
                print("Não houve redirecionamento após clicar na imagem.")

    time.sleep(5)
    driver.quit()


product = "Coloração Igora Royal 8.77 Louro Claro Cobre Extra 60g"

sites = [
    {"url": "https://www.ikesaki.com.br/"},
]

for site in sites:
    search_product_on_site(site["url"], product)
