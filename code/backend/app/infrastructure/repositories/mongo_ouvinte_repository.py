from typing import Optional

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.domain.entities.ouvinte import Ouvinte
from app.domain.repositories.ouvinte_repository import OuvinteRepository


class MongoOuvinteRepository(OuvinteRepository):
    def __init__(self, database: AsyncIOMotorDatabase) -> None:
        self._collection = database["ouvintes"]

    async def create(self, ouvinte: Ouvinte) -> Ouvinte:
        doc = ouvinte.model_dump(by_alias=True, exclude={"id"})
        result = await self._collection.insert_one(doc)
        ouvinte.id = str(result.inserted_id)
        return ouvinte

    async def get_by_id(self, ouvinte_id: str) -> Optional[Ouvinte]:
        if not ObjectId.is_valid(ouvinte_id):
            return None
        doc = await self._collection.find_one({"_id": ObjectId(ouvinte_id)})
        return Ouvinte(**doc) if doc else None

    async def get_by_email(self, email: str) -> Optional[Ouvinte]:
        doc = await self._collection.find_one({"email": email})
        return Ouvinte(**doc) if doc else None
