from typing import List

from dotenv import load_dotenv
from fastapi import APIRouter, Query
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


@router.get("/extract/backhoe_all/")
async def extract_backhoe_all(urls: List[str] = Query(...)):
    e = BackhoeExtract(urls)
    result = e.extract()
    return {"result": result}
