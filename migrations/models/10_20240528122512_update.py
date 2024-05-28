from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "backhoetable" ALTER COLUMN "description" TYPE VARCHAR(600) USING "description"::VARCHAR(600);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "backhoetable" ALTER COLUMN "description" TYPE VARCHAR(255) USING "description"::VARCHAR(255);"""
