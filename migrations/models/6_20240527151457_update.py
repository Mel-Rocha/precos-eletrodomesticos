from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "backhoetable" ALTER COLUMN "worked_hours" TYPE INT USING "worked_hours"::INT;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "backhoetable" ALTER COLUMN "worked_hours" TYPE DECIMAL(10,2) USING "worked_hours"::DECIMAL(10,2);
        ALTER TABLE "backhoetable" ALTER COLUMN "worked_hours" TYPE DECIMAL(10,2) USING "worked_hours"::DECIMAL(10,2);"""
