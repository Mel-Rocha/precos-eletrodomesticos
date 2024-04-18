from tortoise.contrib.pydantic import pydantic_model_creator

from apps.shopping_cart.models import ShoppingCart

ShoppingCartSchema = None


def initialize_shopping_cart_schema():
    global ShoppingCartSchema
    ShoppingCartSchema = pydantic_model_creator(ShoppingCart)


initialize_shopping_cart_schema()
