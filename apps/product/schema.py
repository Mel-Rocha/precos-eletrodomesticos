from tortoise.contrib.pydantic import pydantic_model_creator

from apps.product.models import Product

ProductSchema = None


def initialize_product_schema():
    global ProductSchema
    ProductSchema = pydantic_model_creator(Product)


initialize_product_schema()
