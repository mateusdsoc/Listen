from dataclasses import dataclass

from app.application.exceptions import NotFoundError
from app.domain.entities.sessao import Sessao, StatusSessao
from app.domain.events.eventos_sessao import sessao_criada
from app.domain.events.publisher import EventPublisher
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
        event_publisher: EventPublisher,
    ) -> None:
        self._sessao_repo = sessao_repo
        self._solicitante_repo = solicitante_repo
        self._publisher = event_publisher

    async def execute(self, data: CriarSessaoInput) -> Sessao:
        if not await self._solicitante_repo.get_by_id(data.solicitante_id):
            raise NotFoundError("Solicitante não encontrado")

        sessao = Sessao(
            solicitante_id=data.solicitante_id,
            descricao=data.descricao,
            status=StatusSessao.PENDENTE,
        )
        criada = await self._sessao_repo.create(sessao)

        await self._publisher.publish(
            sessao_criada(
                sessao_id=str(criada.id),
                solicitante_id=str(criada.solicitante_id),
                descricao=criada.descricao,
            )
        )
        return criada
