from fastapi_pagination import Page, add_pagination, paginate
from fastapi import APIRouter

from apps.WishList.models import WishList
from apps.WishList.schema import WishListSchema

router = APIRouter()


@router.get("/")
async def get_shopping_cart_all() -> Page[WishListSchema]:
    shopping_cart_all = await WishList.all()

    return paginate(shopping_cart_all)


add_pagination(router)