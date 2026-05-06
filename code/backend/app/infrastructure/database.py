from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.core.config import settings


class MongoDB:
    client: AsyncIOMotorClient | None = None
    database: AsyncIOMotorDatabase | None = None


db = MongoDB()


async def connect_to_mongo() -> None:
    db.client = AsyncIOMotorClient(settings.mongodb_uri)
    db.database = db.client[settings.mongodb_db_name]
    await db.database["solicitantes"].create_index("email", unique=True)
    await db.database["ouvintes"].create_index("email", unique=True)
    await db.database["sessoes"].create_index("status")
    await db.database["sessoes"].create_index("solicitante_id")


async def close_mongo_connection() -> None:
    if db.client is not None:
        db.client.close()


def get_database() -> AsyncIOMotorDatabase:
    if db.database is None:
        raise RuntimeError("MongoDB não foi inicializado")
    return db.database
