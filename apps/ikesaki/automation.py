import time
import logging

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from tenacity import stop_after_attempt, retry
from selenium.common import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from apps.core.base_automation import CoreAutomation

logging.basicConfig(level=logging.INFO)


class IkesakiAutomation(CoreAutomation):
    """
    Objetivo: Iterar sobre todos anúncios da respectiva máquina e coletar suas URLs específicas.

    Retorno: tupla contendo:
        1 - current_url_all: Lista com todas URLs correspondente a cada anúncio.
        2 - metrics: Lista de dicionários contendo dados de monitoramento da extração.
        3 - automation_failure_analysis: lista de dicionários contendo o xpath específico onde não foi possível obter
        a URL.
    """

    def __init__(self):
        super().__init__()
        self.old_len = 0
        self.metrics = []
        self.automation_failure_analysis = []

    @staticmethod
    def automation_validation(page_number, num_div_elements, current_url_all, old_len):
        num_urls_extracted = len(current_url_all) - old_len
        print(f"Número da Página: {page_number}")
        print(f"Quantidade de Produtos: {num_div_elements}")
        print(f"Quantidade de URLs extraídas: {num_urls_extracted}")

        validation_dict = {
            'page_number': page_number,
            'ads_found': num_div_elements,
            'extracted_urls': num_urls_extracted
        }

        return validation_dict

    @retry(stop=stop_after_attempt(3))
    def ikesaki_url_all(self, generic_product="esmalte risque", site_domain="https://www.ikesaki.com.br"):
        current_url_all = []
        page_number = 1

        try:
            # Search for the product
            search_url = f"{site_domain}/{generic_product}?_q={generic_product}&map=ft"
            self.driver.get(search_url)
            print(search_url)

            while True:
                # Construct the URL with the page number
                url_page_list = f"{search_url}&page={page_number}"

                self.driver.get(url_page_list)
                time.sleep(2)

                html_content = self.driver.page_source
                soup = BeautifulSoup(html_content, 'html.parser')
                gallery_div = soup.find('div', {'id': 'gallery-layout-container'})

                # If no products are found, break the loop
                if not gallery_div:
                    break

                # Retrieves all and entire search results
                img_elements = gallery_div.find_all('img')
                num_div_elements = len(img_elements)
                if num_div_elements == 0:
                    break

                self.old_len = len(current_url_all)

                for i, img in enumerate(img_elements, start=1):
                    img_xpath = (f'//*[@id="gallery-layout-container"]/div[{i}]/section/a/article/div[1]/div['
                                 f'1]/div/div/img')

                    # Find and click on each result
                    try:
                        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, img_xpath)))
                        img_element = self.driver.find_element(By.XPATH, img_xpath)
                        self.driver.execute_script("arguments[0].click();", img_element)  # Solving problem of
                        # intercepted elements
                        current_url_all.append(self.driver.current_url)
                    except TimeoutException as e:
                        print(f"Erro ao clicar na imagem: Tempo de execução limite {e}")
                        logging.error("O elemento foi encontrado, mas não se tornou visivel dentro do tempo limite.")
                        self.automation_failure_analysis.append(img_xpath)
                        continue
                    except NoSuchElementException as e:
                        print(f"Erro ao clicar na imagem: Imagem não encontrada {e}.")
                        logging.error("O elemento não foi encontrado.")
                        self.automation_failure_analysis.append(img_xpath)
                        continue

                    # Returning to the all product listing page
                    self.driver.back()
                    time.sleep(2)

                metrics = self.automation_validation(page_number, num_div_elements, current_url_all,
                                                     self.old_len)
                self.metrics.append(metrics)

                # Advance to the next page
                page_number += 1
                print(self.driver.current_url)
        finally:
            super().stop_driver()

            print(self.metrics)
            logging.info(current_url_all)
            return current_url_all, self.metrics, self.automation_failure_analysis


if __name__ == "__main__":
    a = IkesakiAutomation()
    access = a.ikesaki_url_all("shampoo")
