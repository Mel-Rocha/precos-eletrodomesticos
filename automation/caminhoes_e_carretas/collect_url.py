import time
import logging

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.common import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from automation.core_automation.base_automation import CoreAutomation

logging.basicConfig(level=logging.INFO)


class CaminhoesECarretasAutomation(CoreAutomation):
    """
    Objetivo: Iterar sobre todos anúncios da respectiva máquina e coletar sua url específica.

    Resultado: Lista com todas urls da máquina
    """

    def backhoe_url_all(self):
        self.driver.get("https://www.caminhoesecarretas.com.br/venda/retro%20escavadeira/24?page=0")
        current_url_all = []
        page_number = 0

        try:
            while True:
                url_page_list = f"https://www.caminhoesecarretas.com.br/venda/retro%20escavadeira/24?page={page_number}"
                self.driver.get(url_page_list)
                time.sleep(2)

                html_content = self.driver.page_source
                soup = BeautifulSoup(html_content, 'html.parser')

                all_product = soup.find('div', class_=['productList', 'product-load-more'])
                if not all_product:
                    break

                div_elements = all_product.find_all('div', class_='item-veiculo')
                num_div_elements = len(div_elements)
                print(f"Number of div elements found: {num_div_elements}")
                if num_div_elements == 0:
                    break

                if div_elements:
                    for i, img in enumerate(div_elements, start=0):
                        img_xpath = (f'//*[@id="ContentPlaceHolder1_lvVeiculo_lnkVeiculo_{i}"]/img')
                        logging.info(img_xpath)

                        try:
                            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, img_xpath)))
                            img_element = self.driver.find_element(By.XPATH, img_xpath)
                            logging.info(self.driver.current_url)
                            self.driver.execute_script("arguments[0].click();", img_element)
                            time.sleep(3)
                            current_url_all.append(self.driver.current_url)
                            logging.info(current_url_all)
                        except TimeoutException as e:
                            print(f"Erro ao clicar na imagem: Tempo de execução limite {e}")
                            logging.error("O elemento foi encontrado, mas não se tornou visivel dentro do tempo limite.")
                            continue
                        except NoSuchElementException as e:
                            print(f"Erro ao clicar na imagem: Imagem não encontrada {e}.")
                            logging.error("O elemento não foi encontrado.")
                            continue

                        self.driver.back()
                        time.sleep(2)

                page_number += 1
        finally:
            super().stop_driver()

            print(f'Quantidade de Veículos: {len(current_url_all)} URLS: {current_url_all}')
            return current_url_all


if __name__ == "__main__":
    a = CaminhoesECarretasAutomation()
    access = a.backhoe_url_all()
