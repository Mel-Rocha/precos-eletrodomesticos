import logging

from automation.core_automation.base_automation import CoreAutomation

logging.basicConfig(level=logging.INFO)


class CaminhoesECarretasAutomation(CoreAutomation):
    """
    Objetivo: Cada método sufixado com url_all, deve iterar sobre cada máquina alvo do crawling,
    clicar em todas as combinações possíveis de marca e modelo para a máquina e pesquisa-lá. Então como retorno
    devolver uma lista com cada url especifica.
    """

    @staticmethod
    def combine_harvester_url_all():
        pass

    @staticmethod
    def backhoe_url_all():
        pass

    @staticmethod
    def loader_url_all():
        pass

    @staticmethod
    def small_loader_url_all():
        pass

    @staticmethod
    def mini_excavator_url_all():
        pass

    @staticmethod
    def crawler_tractor_url_all():
        pass

    def test_access_url(self):
        self.driver.get("https://www.caminhoesecarretas.com.br/")


if __name__ == "__main__":
    a = CaminhoesECarretasAutomation()
    test = a.test_access_url()