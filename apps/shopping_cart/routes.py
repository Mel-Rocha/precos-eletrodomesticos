from fastapi_pagination import Page, add_pagination, paginate
from fastapi import APIRouter

from apps.shopping_cart.models import ShoppingCart
from apps.shopping_cart.schema import ShoppingCartSchema

router = APIRouter()


@router.get("/")
async def get_shopping_cart_all() -> Page[ShoppingCartSchema]:
    shopping_cart_all = await ShoppingCart.all()

    return paginate(shopping_cart_all)


add_pagination(router)