from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "wishlist" ALTER COLUMN "need_to_acquire" SET DEFAULT '3';
        ALTER TABLE "wishlist" ALTER COLUMN "desire_to_acquire" SET DEFAULT '3';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "wishlist" ALTER COLUMN "need_to_acquire" SET DEFAULT 'average';
        ALTER TABLE "wishlist" ALTER COLUMN "desire_to_acquire" SET DEFAULT 'average';"""
