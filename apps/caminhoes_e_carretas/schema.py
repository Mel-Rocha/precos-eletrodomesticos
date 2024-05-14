from tortoise.contrib.pydantic import pydantic_model_creator

from apps.caminhoes_e_carretas.models import CaminhoesECarretas

CaminhoesECarretasSchemaWithotFormattedDates = None


def initialize_caminhoes_e_carretas_schema():
    global CaminhoesECarretasSchemaWithotFormattedDates
    CaminhoesECarretasSchemaWithotFormattedDates = pydantic_model_creator(CaminhoesECarretas, exclude=('created_at',
                                                                                                       'updated_at'))


initialize_caminhoes_e_carretas_schema()


class CaminhoesECarretasSchema(CaminhoesECarretasSchemaWithotFormattedDates):
    formatted_created_at: str
    formatted_updated_at: str

    class Config:
        orm_mode = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.formatted_created_at = self.created_at.strftime('%d/%m/%Y %H:%M:%S') if self.created_at else None
        self.formatted_updated_at = self.updated_at.strftime('%d/%m/%Y %H:%M:%S') if self.updated_at else None
