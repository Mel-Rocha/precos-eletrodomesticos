from fastapi import APIRouter
from fastapi_pagination import Page, paginate, add_pagination

from apps.core.models import IkesakiTable
from apps.core.schema import IkesakiTableSchema

router = APIRouter()


@router.get("/")
async def get_ikesaki_all() -> Page[IkesakiTableSchema]:
    ikesaki_all = await IkesakiTable.all().values()
    return paginate(ikesaki_all)


add_pagination(router)
