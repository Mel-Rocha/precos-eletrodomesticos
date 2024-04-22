from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "wishlist" ADD "product_id" UUID;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "wishlist" DROP COLUMN "product_id";"""
