from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.domain.entities.sessao import Avaliacao, Sessao, StatusSessao


class SessaoCreateRequest(BaseModel):
    solicitante_id: str
    descricao: str = Field(min_length=1, max_length=2000)


class SessaoStatusUpdateRequest(BaseModel):
    status: StatusSessao
    ouvinte_id: Optional[str] = None


class SessaoResponse(BaseModel):
    id: str
    solicitante_id: str
    ouvinte_id: Optional[str] = None
    descricao: str
    status: StatusSessao
    avaliacao: Optional[Avaliacao] = None
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, entity: Sessao) -> "SessaoResponse":
        return cls(
            id=str(entity.id),
            solicitante_id=str(entity.solicitante_id),
            ouvinte_id=str(entity.ouvinte_id) if entity.ouvinte_id else None,
            descricao=entity.descricao,
            status=entity.status,
            avaliacao=entity.avaliacao,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
