from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from .common import PyObjectId


class Ouvinte(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    primeiro_nome: str
    email: EmailStr
    senha: str
    instituicao: str
    periodo: int = Field(ge=1, le=12)
    disponivel: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
