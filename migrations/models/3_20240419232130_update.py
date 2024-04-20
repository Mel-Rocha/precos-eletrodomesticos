from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "wishlist" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "product_name" VARCHAR(255) NOT NULL,
    "site_domain" VARCHAR(255) NOT NULL,
    "expected_purchase_date" DATE NOT NULL,
    "desire_to_acquire" VARCHAR(10) NOT NULL  DEFAULT 'average',
    "need_to_acquire" VARCHAR(10) NOT NULL  DEFAULT 'average'
);
        DROP TABLE IF EXISTS "shoppingcart";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "wishlist";"""
