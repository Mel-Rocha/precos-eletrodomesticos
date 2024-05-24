from fastapi import APIRouter
from fastapi_pagination import Page, paginate, add_pagination

from apps.core.models import BackhoeTable
from apps.core.schema import BackhoeTableSchema

router = APIRouter()


@router.get("/")
async def get_backhoe_all() -> Page[BackhoeTableSchema]:
    caminhoes_e_carretas_all = await BackhoeTable.all().values()
    return paginate(caminhoes_e_carretas_all)


add_pagination(router)
