from dataclasses import dataclass
from enum import Enum
from typing import Tuple

from app.application.exceptions import AuthenticationError
from app.core.security import create_access_token, verify_password
from app.domain.repositories.ouvinte_repository import OuvinteRepository
from app.domain.repositories.solicitante_repository import SolicitanteRepository


class Role(str, Enum):
    SOLICITANTE = "solicitante"
    OUVINTE = "ouvinte"


@dataclass
class LoginInput:
    email: str
    senha: str
    role: Role


@dataclass
class LoginOutput:
    access_token: str
    token_type: str
    user_id: str
    nome: str
    email: str
    role: str


class LoginUseCase:
    def __init__(
        self,
        solicitante_repo: SolicitanteRepository,
        ouvinte_repo: OuvinteRepository,
    ) -> None:
        self._solicitante_repo = solicitante_repo
        self._ouvinte_repo = ouvinte_repo

    async def execute(self, data: LoginInput) -> LoginOutput:
        if data.role == Role.SOLICITANTE:
            user = await self._solicitante_repo.get_by_email(data.email)
        else:
            user = await self._ouvinte_repo.get_by_email(data.email)

        if user is None:
            raise AuthenticationError("Email ou senha incorretos")

        if not verify_password(data.senha, user.senha):
            raise AuthenticationError("Email ou senha incorretos")

        token = create_access_token(
            user_id=str(user.id),
            role=data.role.value,
        )

        return LoginOutput(
            access_token=token,
            token_type="bearer",
            user_id=str(user.id),
            nome=user.primeiro_nome,
            email=user.email,
            role=data.role.value,
        )
