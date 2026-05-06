from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from app.domain.entities.ouvinte import Ouvinte


class OuvinteCreateRequest(BaseModel):
    primeiro_nome: str = Field(min_length=1, max_length=80)
    email: EmailStr
    senha: str = Field(min_length=6, max_length=128)
    instituicao: str = Field(min_length=1, max_length=120)
    periodo: int = Field(ge=1, le=12)
    disponivel: bool = True


class OuvinteResponse(BaseModel):
    id: str
    primeiro_nome: str
    email: EmailStr
    instituicao: str
    periodo: int
    disponivel: bool
    created_at: datetime

    @classmethod
    def from_entity(cls, entity: Ouvinte) -> "OuvinteResponse":
        return cls(
            id=str(entity.id),
            primeiro_nome=entity.primeiro_nome,
            email=entity.email,
            instituicao=entity.instituicao,
            periodo=entity.periodo,
            disponivel=entity.disponivel,
            created_at=entity.created_at,
        )
