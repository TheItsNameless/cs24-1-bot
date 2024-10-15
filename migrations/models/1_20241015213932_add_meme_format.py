from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "meme" ADD "format" VARCHAR(3) NOT NULL  /* PNG: png\nGIF: gif */;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "meme" DROP COLUMN "format";"""
