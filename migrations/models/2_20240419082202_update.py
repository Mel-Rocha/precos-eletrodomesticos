from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "shoppingcart" RENAME COLUMN "value" TO "price";
        ALTER TABLE "shoppingcart" RENAME COLUMN "product_name" TO "product";
        ALTER TABLE "shoppingcart" ALTER COLUMN "description" DROP NOT NULL;
        ALTER TABLE "shoppingcart" ALTER COLUMN "description" TYPE VARCHAR(255) USING "description"::VARCHAR(255);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "shoppingcart" RENAME COLUMN "product" TO "product_name";
        ALTER TABLE "shoppingcart" RENAME COLUMN "price" TO "value";
        ALTER TABLE "shoppingcart" ALTER COLUMN "description" TYPE TEXT USING "description"::TEXT;
        ALTER TABLE "shoppingcart" ALTER COLUMN "description" SET NOT NULL;"""
