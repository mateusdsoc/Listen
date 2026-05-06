from abc import ABC, abstractmethod
from typing import Optional

from app.domain.entities.solicitante import Solicitante


class SolicitanteRepository(ABC):
    @abstractmethod
    async def create(self, solicitante: Solicitante) -> Solicitante: ...

    @abstractmethod
    async def get_by_id(self, solicitante_id: str) -> Optional[Solicitante]: ...

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[Solicitante]: ...
