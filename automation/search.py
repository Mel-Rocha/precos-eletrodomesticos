import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class AutomationSearchProduct:
    def __init__(self):
        self.service = Service(ChromeDriverManager().install())
        self.driver = None

    def start_driver(self):
        self.driver = webdriver.Chrome(service=self.service)

    def stop_driver(self):
        if self.driver:
            self.driver.quit()

    def search_product_on_site(self, site_url, product):
        self.start_driver()

        self.driver.get(site_url)
        time.sleep(2)
        search_box = self.driver.find_element('xpath', '//*[@id="downshift-0-input"]')
        search_box.send_keys(product, Keys.ENTER)
        time.sleep(5)

        html_content = self.driver.page_source

        soup = BeautifulSoup(html_content, 'html.parser')

        gallery_div = soup.find('div', {'id': 'gallery-layout-container'})
        if gallery_div:
            first_img = gallery_div.find('img')
            if first_img:
                img_element = self.driver.find_element('xpath', '//*[@id="gallery-layout-container"]/div/section/a/article'
                                                           '/div[1]/div[1]/div/div/img')

                img_element.click()

                time.sleep(3)

                if self.driver.current_url != site_url:
                    print("Redirecionado para:", self.driver.current_url)
                else:
                    print("Não houve redirecionamento após clicar na imagem.")

        time.sleep(5)
        self.stop_driver()

        # return self.driver.current_url


# sites = [
#     {"url": "https://www.ikesaki.com.br/"},
# ]

# product = "Coloração Igora Royal 8.77 Louro Claro Cobre Extra 60g"
# automation = AutomationSearchProduct()
# for site in sites:
#     automation.search_product_on_site(site["url"], product)