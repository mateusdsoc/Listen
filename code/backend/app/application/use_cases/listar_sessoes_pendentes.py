from typing import List

from app.domain.entities.sessao import Sessao, StatusSessao
from app.domain.repositories.sessao_repository import SessaoRepository


class ListarSessoesPendentesUseCase:
    def __init__(self, repo: SessaoRepository) -> None:
        self._repo = repo

    async def execute(self) -> List[Sessao]:
        return await self._repo.list_by_status(StatusSessao.PENDENTE)
