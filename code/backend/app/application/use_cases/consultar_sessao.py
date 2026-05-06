from app.application.exceptions import NotFoundError
from app.domain.entities.sessao import Sessao
from app.domain.repositories.sessao_repository import SessaoRepository


class ConsultarSessaoUseCase:
    def __init__(self, repo: SessaoRepository) -> None:
        self._repo = repo

    async def execute(self, sessao_id: str) -> Sessao:
        sessao = await self._repo.get_by_id(sessao_id)
        if sessao is None:
            raise NotFoundError("Sessão não encontrada")
        return sessao
