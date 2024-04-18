from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "shoppingcart" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "product_name" VARCHAR(255) NOT NULL,
    "description" TEXT NOT NULL,
    "value" DECIMAL(10,2) NOT NULL,
    "store" VARCHAR(50) NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "shoppingcart";"""
