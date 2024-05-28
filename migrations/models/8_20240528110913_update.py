from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE INDEX "idx_backhoetabl_url_ce3d1e" ON "backhoetable" ("url");
        CREATE INDEX "idx_backhoetabl_price_955c58" ON "backhoetable" ("price");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX "idx_backhoetabl_price_955c58";
        DROP INDEX "idx_backhoetabl_url_ce3d1e";"""
