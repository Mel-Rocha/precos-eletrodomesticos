from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX IF EXISTS idx_backhoetabl_url_ce3d1e;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE UNIQUE INDEX "uid_backhoetabl_url_ce3d1e" ON "backhoetable" ("url");"""
