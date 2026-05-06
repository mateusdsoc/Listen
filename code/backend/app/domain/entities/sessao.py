from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from .common import PyObjectId


class StatusSessao(str, Enum):
    PENDENTE = "pendente"
    ACEITA = "aceita"
    EM_ANDAMENTO = "em_andamento"
    CONCLUIDA = "concluida"
    CANCELADA = "cancelada"


class Avaliacao(BaseModel):
    nota: int = Field(ge=1, le=5)
    comentario: Optional[str] = None


class Sessao(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    solicitante_id: PyObjectId
    ouvinte_id: Optional[PyObjectId] = None
    descricao: str
    status: StatusSessao = StatusSessao.PENDENTE
    avaliacao: Optional[Avaliacao] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
