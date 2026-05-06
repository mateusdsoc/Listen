from dataclasses import dataclass
from typing import Optional, Set

from app.application.exceptions import (
    InvalidStateTransitionError,
    NotFoundError,
    ValidationError,
)
from app.domain.entities.sessao import Sessao, StatusSessao
from app.domain.repositories.ouvinte_repository import OuvinteRepository
from app.domain.repositories.sessao_repository import SessaoRepository


_TRANSICOES_VALIDAS: dict[StatusSessao, Set[StatusSessao]] = {
    StatusSessao.PENDENTE: {StatusSessao.ACEITA, StatusSessao.CANCELADA},
    StatusSessao.ACEITA: {StatusSessao.EM_ANDAMENTO, StatusSessao.CANCELADA},
    StatusSessao.EM_ANDAMENTO: {StatusSessao.CONCLUIDA, StatusSessao.CANCELADA},
    StatusSessao.CONCLUIDA: set(),
    StatusSessao.CANCELADA: set(),
}


@dataclass
class AtualizarStatusSessaoInput:
    sessao_id: str
    novo_status: StatusSessao
    ouvinte_id: Optional[str] = None


class AtualizarStatusSessaoUseCase:
    def __init__(
        self,
        sessao_repo: SessaoRepository,
        ouvinte_repo: OuvinteRepository,
    ) -> None:
        self._sessao_repo = sessao_repo
        self._ouvinte_repo = ouvinte_repo

    async def execute(self, data: AtualizarStatusSessaoInput) -> Sessao:
        sessao = await self._sessao_repo.get_by_id(data.sessao_id)
        if sessao is None:
            raise NotFoundError("Sessão não encontrada")

        permitidos = _TRANSICOES_VALIDAS[sessao.status]
        if data.novo_status not in permitidos:
            raise InvalidStateTransitionError(
                f"Transição inválida: {sessao.status.value} -> {data.novo_status.value}"
            )

        ouvinte_id = data.ouvinte_id
        if data.novo_status == StatusSessao.ACEITA:
            if not ouvinte_id:
                raise ValidationError("ouvinte_id é obrigatório ao aceitar a sessão")
            if not await self._ouvinte_repo.get_by_id(ouvinte_id):
                raise NotFoundError("Ouvinte não encontrado")
        else:
            ouvinte_id = None

        atualizada = await self._sessao_repo.update_status(
            sessao_id=data.sessao_id,
            status=data.novo_status,
            ouvinte_id=ouvinte_id,
        )
        if atualizada is None:
            raise NotFoundError("Sessão não encontrada")
        return atualizada
