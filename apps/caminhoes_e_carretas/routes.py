from dotenv import load_dotenv
from fastapi import APIRouter
from fastapi_pagination import Page, add_pagination, paginate

from apps.caminhoes_e_carretas.models import CaminhoesECarretas
from apps.caminhoes_e_carretas.schema import CaminhoesECarretasSchema


load_dotenv()

router = APIRouter()


@router.get("/")
async def get_caminhoes_e_carretas_all() -> Page[CaminhoesECarretasSchema]:
    caminhoes_e_carretas_all = await CaminhoesECarretas.all().values()
    return paginate(caminhoes_e_carretas_all)


add_pagination(router)