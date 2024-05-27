from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "backhoetable" ALTER COLUMN "price" TYPE BIGINT USING "price"::BIGINT;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "backhoetable" ALTER COLUMN "price" TYPE DECIMAL(10,2) USING "price"::DECIMAL(10,2);
        ALTER TABLE "backhoetable" ALTER COLUMN "price" TYPE DECIMAL(10,2) USING "price"::DECIMAL(10,2);"""
