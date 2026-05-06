from typing import Optional

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.domain.entities.solicitante import Solicitante
from app.domain.repositories.solicitante_repository import SolicitanteRepository


class MongoSolicitanteRepository(SolicitanteRepository):
    def __init__(self, database: AsyncIOMotorDatabase) -> None:
        self._collection = database["solicitantes"]

    async def create(self, solicitante: Solicitante) -> Solicitante:
        doc = solicitante.model_dump(by_alias=True, exclude={"id"})
        result = await self._collection.insert_one(doc)
        solicitante.id = str(result.inserted_id)
        return solicitante

    async def get_by_id(self, solicitante_id: str) -> Optional[Solicitante]:
        if not ObjectId.is_valid(solicitante_id):
            return None
        doc = await self._collection.find_one({"_id": ObjectId(solicitante_id)})
        return Solicitante(**doc) if doc else None

    async def get_by_email(self, email: str) -> Optional[Solicitante]:
        doc = await self._collection.find_one({"email": email})
        return Solicitante(**doc) if doc else None
