from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "caminhoesecarretas" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "crawl_date" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "fabricator" VARCHAR(255) NOT NULL,
    "model" VARCHAR(255) NOT NULL,
    "year_fabrication" INT NOT NULL  DEFAULT 0,
    "price" DECIMAL(10,2) NOT NULL,
    "url" VARCHAR(255) NOT NULL,
    "worked_hours" DECIMAL(5,2) NOT NULL,
    "state" VARCHAR(255) NOT NULL,
    "date_of_posting" TIMESTAMPTZ NOT NULL,
    "is_combine_harvester" BOOL NOT NULL  DEFAULT True,
    "is_backhoe" BOOL NOT NULL  DEFAULT False,
    "is_loader" BOOL NOT NULL  DEFAULT False,
    "is_small_loader" BOOL NOT NULL  DEFAULT False,
    "is_mini_excavator" BOOL NOT NULL  DEFAULT False,
    "is_crawler_tractor" BOOL NOT NULL  DEFAULT False
);
CREATE TABLE IF NOT EXISTS "coretable" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "crawl_date" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "fabricator" VARCHAR(255) NOT NULL,
    "model" VARCHAR(255) NOT NULL,
    "year_fabrication" INT NOT NULL  DEFAULT 0,
    "price" DECIMAL(10,2) NOT NULL,
    "url" VARCHAR(255) NOT NULL,
    "worked_hours" DECIMAL(5,2) NOT NULL,
    "state" VARCHAR(255) NOT NULL,
    "date_of_posting" TIMESTAMPTZ NOT NULL,
    "is_combine_harvester" BOOL NOT NULL  DEFAULT True,
    "is_backhoe" BOOL NOT NULL  DEFAULT False,
    "is_loader" BOOL NOT NULL  DEFAULT False,
    "is_small_loader" BOOL NOT NULL  DEFAULT False,
    "is_mini_excavator" BOOL NOT NULL  DEFAULT False,
    "is_crawler_tractor" BOOL NOT NULL  DEFAULT False
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
