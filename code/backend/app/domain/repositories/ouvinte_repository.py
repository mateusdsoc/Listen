from abc import ABC, abstractmethod
from typing import Optional

from app.domain.entities.ouvinte import Ouvinte


class OuvinteRepository(ABC):
    @abstractmethod
    async def create(self, ouvinte: Ouvinte) -> Ouvinte: ...

    @abstractmethod
    async def get_by_id(self, ouvinte_id: str) -> Optional[Ouvinte]: ...

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[Ouvinte]: ...
