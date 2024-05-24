from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "backhoetable" ALTER COLUMN "volume" TYPE DECIMAL(10,2) USING "volume"::DECIMAL(10,2);
        ALTER TABLE "backhoetable" ALTER COLUMN "length" TYPE DECIMAL(10,2) USING "length"::DECIMAL(10,2);
        ALTER TABLE "backhoetable" ALTER COLUMN "worked_hours" TYPE DECIMAL(10,2) USING "worked_hours"::DECIMAL(10,2);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "backhoetable" ALTER COLUMN "volume" TYPE DECIMAL(5,2) USING "volume"::DECIMAL(5,2);
        ALTER TABLE "backhoetable" ALTER COLUMN "length" TYPE DECIMAL(5,2) USING "length"::DECIMAL(5,2);
        ALTER TABLE "backhoetable" ALTER COLUMN "worked_hours" TYPE DECIMAL(5,2) USING "worked_hours"::DECIMAL(5,2);"""
