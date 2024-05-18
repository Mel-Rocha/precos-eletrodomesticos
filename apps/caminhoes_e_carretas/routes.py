from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from fastapi_pagination import Page, add_pagination, paginate

from apps.caminhoes_e_carretas.models import CaminhoesECarretas
from apps.caminhoes_e_carretas.schema import CaminhoesECarretasSchema
from scraping.caminhoes_e_carretas.backhoe import BackhoeExtract

load_dotenv()

router = APIRouter()


@router.get("/")
async def get_caminhoes_e_carretas_all() -> Page[CaminhoesECarretasSchema]:
    caminhoes_e_carretas_all = await CaminhoesECarretas.all().values()
    return paginate(caminhoes_e_carretas_all)


add_pagination(router)


@router.get("/extract/specific/")
async def extract_backhoe_info(url: str):
    e = BackhoeExtract(url)
    return e.extract()
