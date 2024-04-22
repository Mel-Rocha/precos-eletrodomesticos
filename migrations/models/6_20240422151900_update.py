from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "wishlist" ADD "wish_title" VARCHAR(255) NOT NULL;
        ALTER TABLE "wishlist" DROP COLUMN "product_name";
        ALTER TABLE "wishlist" DROP COLUMN "site_domain";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "wishlist" ADD "product_name" VARCHAR(255) NOT NULL;
        ALTER TABLE "wishlist" ADD "site_domain" VARCHAR(255) NOT NULL;
        ALTER TABLE "wishlist" DROP COLUMN "wish_title";"""
