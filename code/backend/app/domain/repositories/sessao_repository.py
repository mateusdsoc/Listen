from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities.sessao import Sessao, StatusSessao


class SessaoRepository(ABC):
    @abstractmethod
    async def create(self, sessao: Sessao) -> Sessao: ...

    @abstractmethod
    async def get_by_id(self, sessao_id: str) -> Optional[Sessao]: ...

    @abstractmethod
    async def list_by_status(self, status: StatusSessao) -> List[Sessao]: ...

    @abstractmethod
    async def update_status(
        self,
        sessao_id: str,
        status: StatusSessao,
        ouvinte_id: Optional[str] = None,
    ) -> Optional[Sessao]: ...
