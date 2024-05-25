from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "backhoetable" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "price" DECIMAL(10,2) NOT NULL,
    "url" VARCHAR(255) NOT NULL UNIQUE,
    "crawl_date" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "fabricator" VARCHAR(255),
    "model" VARCHAR(255),
    "year_fabrication" INT,
    "worked_hours" DECIMAL(5,2),
    "state" VARCHAR(255),
    "date_of_posting" TIMESTAMPTZ,
    "length" DECIMAL(5,2),
    "volume" DECIMAL(5,2),
    "pallets" INT,
    "model_code" VARCHAR(50)
);
        DROP TABLE IF EXISTS "caminhoesecarretas";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "backhoetable";"""
