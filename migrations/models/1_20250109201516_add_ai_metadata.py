from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "aimetadata" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "usage_today" INT NOT NULL  /* The number of requests used today */,
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
) /* A class representing metadata for the AI service. */;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "aimetadata";"""
