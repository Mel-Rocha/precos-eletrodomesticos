import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class AutomationSearchProduct:
    def __init__(self):
        self.service = Service(ChromeDriverManager().install())
        self.driver = None

    def start_driver(self):
        self.driver = webdriver.Chrome(service=self.service)

    def stop_driver(self):
        if self.driver:
            self.driver.quit()

    def search_product_on_site(self, product, site_domain="https://www.ikesaki.com.br/"):
        self.start_driver()

        self.driver.get(site_domain)
        time.sleep(2)
        search_box = self.driver.find_element('xpath', '//*[@id="downshift-0-input"]')
        search_box.send_keys(product, Keys.ENTER)
        time.sleep(5)

        urls = []

        while True:
            html_content = self.driver.page_source
            soup = BeautifulSoup(html_content, 'html.parser')
            gallery_div = soup.find('div', {'id': 'gallery-layout-container'})

            if gallery_div:
                img_elements = gallery_div.find_all('img')
                for i, img in enumerate(img_elements, start=1):
                    img_xpath = f'//*[@id="gallery-layout-container"]/div[{i}]/section/a/article/div[1]/div[1]/div/div/img'

                    # Aguarda até que o elemento esteja visível
                    WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, img_xpath)))

                    img_element = self.driver.find_element('xpath', img_xpath)

                    try:
                        # Execute um script JavaScript para clicar no elemento
                        self.driver.execute_script("arguments[0].click();", img_element)
                    except Exception as e:
                        print(f"Erro ao clicar na imagem: {e}")
                        continue

                    time.sleep(3)

                    try:
                        if self.driver.current_url != site_domain:
                            print("Redirecionado para:", self.driver.current_url)
                            urls.append(self.driver.current_url)
                        else:
                            print("Não houve redirecionamento após clicar na imagem.")
                    except Exception as e:
                        print(f"Erro ao obter a URL atual: {e}")
                        continue

                    # Volta para a página anterior para clicar na próxima imagem
                    self.driver.back()
                    time.sleep(2)

                # Verifica se há próximo botão de página e clica nele
            next_page_button = self.driver.find_element('xpath', '//*[@aria-label="Next"]')
            if next_page_button.get_attribute('aria-disabled') == 'true':
                break
            else:
                next_page_button.click()
                time.sleep(5)

        self.stop_driver()

        return urls

    @staticmethod
    def get_xpath_of_element(element):
        """Obtém o XPath de um elemento BeautifulSoup"""
        path = []
        parent = element.parent
        while parent:
            if parent.name:
                path.insert(0, parent.name)
            parent = parent.parent
        return '/'.join(path)