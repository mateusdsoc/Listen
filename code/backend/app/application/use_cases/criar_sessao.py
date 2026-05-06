from dataclasses import dataclass

from app.application.exceptions import NotFoundError
from app.domain.entities.sessao import Sessao, StatusSessao
from app.domain.repositories.sessao_repository import SessaoRepository
from app.domain.repositories.solicitante_repository import SolicitanteRepository


@dataclass
class CriarSessaoInput:
    solicitante_id: str
    descricao: str


class CriarSessaoUseCase:
    def __init__(
        self,
        sessao_repo: SessaoRepository,
        solicitante_repo: SolicitanteRepository,
    ) -> None:
        self._sessao_repo = sessao_repo
        self._solicitante_repo = solicitante_repo

    async def execute(self, data: CriarSessaoInput) -> Sessao:
        if not await self._solicitante_repo.get_by_id(data.solicitante_id):
            raise NotFoundError("Solicitante não encontrado")

        sessao = Sessao(
            solicitante_id=data.solicitante_id,
            descricao=data.descricao,
            status=StatusSessao.PENDENTE,
        )
        return await self._sessao_repo.create(sessao)
