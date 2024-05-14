import logging

logging.basicConfig(level=logging.INFO)


class CaminhoesECarretasExtract:
    """
    Objetivo: Com base na url especifica fazer a extração das informações relevantes
    """

    def __init__(self, url_specific):
        self.url_specific = url_specific
