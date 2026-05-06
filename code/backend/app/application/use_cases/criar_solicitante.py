from dataclasses import dataclass

from app.application.exceptions import ConflictError
from app.core.security import hash_password
from app.domain.entities.solicitante import Solicitante
from app.domain.repositories.solicitante_repository import SolicitanteRepository


@dataclass
class CriarSolicitanteInput:
    primeiro_nome: str
    email: str
    senha: str


class CriarSolicitanteUseCase:
    def __init__(self, repo: SolicitanteRepository) -> None:
        self._repo = repo

    async def execute(self, data: CriarSolicitanteInput) -> Solicitante:
        if await self._repo.get_by_email(data.email):
            raise ConflictError("Já existe um solicitante com este email")

        solicitante = Solicitante(
            primeiro_nome=data.primeiro_nome,
            email=data.email,
            senha=hash_password(data.senha),
        )
        return await self._repo.create(solicitante)
