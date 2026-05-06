from datetime import datetime
from typing import List, Optional

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.domain.entities.sessao import Sessao, StatusSessao
from app.domain.repositories.sessao_repository import SessaoRepository


def _to_object_id(value: Optional[str]) -> Optional[ObjectId]:
    return ObjectId(value) if value and ObjectId.is_valid(value) else None


class MongoSessaoRepository(SessaoRepository):
    def __init__(self, database: AsyncIOMotorDatabase) -> None:
        self._collection = database["sessoes"]

    async def create(self, sessao: Sessao) -> Sessao:
        doc = sessao.model_dump(by_alias=True, exclude={"id"})
        doc["solicitante_id"] = ObjectId(sessao.solicitante_id)
        if sessao.ouvinte_id:
            doc["ouvinte_id"] = ObjectId(sessao.ouvinte_id)
        doc["status"] = sessao.status.value
        result = await self._collection.insert_one(doc)
        sessao.id = str(result.inserted_id)
        return sessao

    async def get_by_id(self, sessao_id: str) -> Optional[Sessao]:
        if not ObjectId.is_valid(sessao_id):
            return None
        doc = await self._collection.find_one({"_id": ObjectId(sessao_id)})
        return self._to_entity(doc) if doc else None

    async def list_by_status(self, status: StatusSessao) -> List[Sessao]:
        cursor = self._collection.find({"status": status.value}).sort("created_at", 1)
        return [self._to_entity(doc) async for doc in cursor]

    async def update_status(
        self,
        sessao_id: str,
        status: StatusSessao,
        ouvinte_id: Optional[str] = None,
    ) -> Optional[Sessao]:
        if not ObjectId.is_valid(sessao_id):
            return None

        update: dict = {
            "status": status.value,
            "updated_at": datetime.utcnow(),
        }
        if ouvinte_id is not None:
            update["ouvinte_id"] = ObjectId(ouvinte_id)

        doc = await self._collection.find_one_and_update(
            {"_id": ObjectId(sessao_id)},
            {"$set": update},
            return_document=True,
        )
        return self._to_entity(doc) if doc else None

    @staticmethod
    def _to_entity(doc: dict) -> Sessao:
        normalized = dict(doc)
        if isinstance(normalized.get("solicitante_id"), ObjectId):
            normalized["solicitante_id"] = str(normalized["solicitante_id"])
        if isinstance(normalized.get("ouvinte_id"), ObjectId):
            normalized["ouvinte_id"] = str(normalized["ouvinte_id"])
        return Sessao(**normalized)
