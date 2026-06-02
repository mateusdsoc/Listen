from typing import List

from app.domain.entities.sessao import Sessao
from app.domain.repositories.sessao_repository import SessaoRepository


class ListarSessoesDoSolicitanteUseCase:
    def __init__(self, repo: SessaoRepository) -> None:
        self._repo = repo

    async def execute(self, solicitante_id: str) -> List[Sessao]:
        return await self._repo.list_by_solicitante(solicitante_id)
