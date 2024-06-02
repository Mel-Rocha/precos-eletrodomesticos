from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "ikesakitable" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "price" BIGINT NOT NULL,
    "url" VARCHAR(255) NOT NULL,
    "crawl_date" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "product" VARCHAR(255)
);
CREATE INDEX IF NOT EXISTS "idx_ikesakitabl_price_aa82b9" ON "ikesakitable" ("price");
CREATE INDEX IF NOT EXISTS "idx_ikesakitabl_url_0bdcab" ON "ikesakitable" ("url");
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
