from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "user" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "global_name" VARCHAR(255) NOT NULL,
    "display_name" VARCHAR(255) NOT NULL
);
CREATE TABLE IF NOT EXISTS "meme" (
    "uuid" CHAR(36) NOT NULL  PRIMARY KEY,
    "message" TEXT NOT NULL,
    "date" TIMESTAMP NOT NULL,
    "author_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSON NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
