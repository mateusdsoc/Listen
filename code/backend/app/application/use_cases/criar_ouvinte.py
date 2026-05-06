from dataclasses import dataclass

from app.application.exceptions import ConflictError
from app.core.security import hash_password
from app.domain.entities.ouvinte import Ouvinte
from app.domain.repositories.ouvinte_repository import OuvinteRepository


@dataclass
class CriarOuvinteInput:
    primeiro_nome: str
    email: str
    senha: str
    instituicao: str
    periodo: int
    disponivel: bool = True


class CriarOuvinteUseCase:
    def __init__(self, repo: OuvinteRepository) -> None:
        self._repo = repo

    async def execute(self, data: CriarOuvinteInput) -> Ouvinte:
        if await self._repo.get_by_email(data.email):
            raise ConflictError("Já existe um ouvinte com este email")

        ouvinte = Ouvinte(
            primeiro_nome=data.primeiro_nome,
            email=data.email,
            senha=hash_password(data.senha),
            instituicao=data.instituicao,
            periodo=data.periodo,
            disponivel=data.disponivel,
        )
        return await self._repo.create(ouvinte)
