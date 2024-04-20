from fastapi_pagination import Page, add_pagination, paginate
from fastapi import APIRouter

from apps.WishList.models import WishList
from apps.WishList.schema import WishListSchema

router = APIRouter()


@router.get("/")
async def get_wish_list_all() -> Page[WishListSchema]:
    wish_list_all = await WishList.all()

    return paginate(wish_list_all)


add_pagination(router)