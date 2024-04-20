from tortoise.contrib.pydantic import pydantic_model_creator

from apps.wish_list.models import WishList

WishListSchema = None


def initialize_wish_list_schema():
    global WishListSchema
    WishListSchema = pydantic_model_creator(WishList)


initialize_wish_list_schema()
