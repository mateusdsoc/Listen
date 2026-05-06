from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from app.domain.entities.solicitante import Solicitante


class SolicitanteCreateRequest(BaseModel):
    primeiro_nome: str = Field(min_length=1, max_length=80)
    email: EmailStr
    senha: str = Field(min_length=6, max_length=128)


class SolicitanteResponse(BaseModel):
    id: str
    primeiro_nome: str
    email: EmailStr
    created_at: datetime

    @classmethod
    def from_entity(cls, entity: Solicitante) -> "SolicitanteResponse":
        return cls(
            id=str(entity.id),
            primeiro_nome=entity.primeiro_nome,
            email=entity.email,
            created_at=entity.created_at,
        )
