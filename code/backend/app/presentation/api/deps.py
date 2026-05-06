from dataclasses import dataclass
from typing import Optional

import jwt
from fastapi import Depends, Header
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.application.exceptions import AuthenticationError
from app.application.use_cases.atualizar_status_sessao import (
    AtualizarStatusSessaoUseCase,
)
from app.application.use_cases.consultar_sessao import ConsultarSessaoUseCase
from app.application.use_cases.criar_ouvinte import CriarOuvinteUseCase
from app.application.use_cases.criar_sessao import CriarSessaoUseCase
from app.application.use_cases.criar_solicitante import CriarSolicitanteUseCase
from app.application.use_cases.listar_sessoes_pendentes import (
    ListarSessoesPendentesUseCase,
)
from app.application.use_cases.login import LoginUseCase
from app.core.security import decode_access_token
from app.domain.repositories.ouvinte_repository import OuvinteRepository
from app.domain.repositories.sessao_repository import SessaoRepository
from app.domain.repositories.solicitante_repository import SolicitanteRepository
from app.infrastructure.database import get_database
from app.infrastructure.repositories.mongo_ouvinte_repository import (
    MongoOuvinteRepository,
)
from app.infrastructure.repositories.mongo_sessao_repository import (
    MongoSessaoRepository,
)
from app.infrastructure.repositories.mongo_solicitante_repository import (
    MongoSolicitanteRepository,
)


# ── Dataclass para o usuário autenticado ────────────────────────────
@dataclass
class CurrentUser:
    user_id: str
    role: str  # "solicitante" | "ouvinte"


# ── Database ────────────────────────────────────────────────────────
def get_db() -> AsyncIOMotorDatabase:
    return get_database()


# ── Repositories ────────────────────────────────────────────────────
def get_solicitante_repo(
    database: AsyncIOMotorDatabase = Depends(get_db),
) -> SolicitanteRepository:
    return MongoSolicitanteRepository(database)


def get_ouvinte_repo(
    database: AsyncIOMotorDatabase = Depends(get_db),
) -> OuvinteRepository:
    return MongoOuvinteRepository(database)


def get_sessao_repo(
    database: AsyncIOMotorDatabase = Depends(get_db),
) -> SessaoRepository:
    return MongoSessaoRepository(database)


# ── Auth dependency ─────────────────────────────────────────────────
async def get_current_user(
    authorization: Optional[str] = Header(default=None),
) -> CurrentUser:
    if not authorization:
        raise AuthenticationError("Token de autenticação não fornecido")

    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        raise AuthenticationError("Formato de token inválido. Use: Bearer <token>")

    try:
        payload = decode_access_token(token)
    except jwt.ExpiredSignatureError:
        raise AuthenticationError("Token expirado")
    except jwt.InvalidTokenError:
        raise AuthenticationError("Token inválido")

    user_id: Optional[str] = payload.get("sub")
    role: Optional[str] = payload.get("role")
    if not user_id or not role:
        raise AuthenticationError("Token com dados incompletos")

    return CurrentUser(user_id=user_id, role=role)


# ── Use Cases ───────────────────────────────────────────────────────
def get_login_uc(
    solicitante_repo: SolicitanteRepository = Depends(get_solicitante_repo),
    ouvinte_repo: OuvinteRepository = Depends(get_ouvinte_repo),
) -> LoginUseCase:
    return LoginUseCase(solicitante_repo, ouvinte_repo)


def get_criar_solicitante_uc(
    repo: SolicitanteRepository = Depends(get_solicitante_repo),
    ouvinte_repo: OuvinteRepository = Depends(get_ouvinte_repo),
) -> CriarSolicitanteUseCase:
    return CriarSolicitanteUseCase(repo, ouvinte_repo)


def get_criar_ouvinte_uc(
    repo: OuvinteRepository = Depends(get_ouvinte_repo),
    solicitante_repo: SolicitanteRepository = Depends(get_solicitante_repo),
) -> CriarOuvinteUseCase:
    return CriarOuvinteUseCase(repo, solicitante_repo)


def get_criar_sessao_uc(
    sessao_repo: SessaoRepository = Depends(get_sessao_repo),
    solicitante_repo: SolicitanteRepository = Depends(get_solicitante_repo),
) -> CriarSessaoUseCase:
    return CriarSessaoUseCase(sessao_repo, solicitante_repo)


def get_listar_pendentes_uc(
    repo: SessaoRepository = Depends(get_sessao_repo),
) -> ListarSessoesPendentesUseCase:
    return ListarSessoesPendentesUseCase(repo)


def get_consultar_sessao_uc(
    repo: SessaoRepository = Depends(get_sessao_repo),
) -> ConsultarSessaoUseCase:
    return ConsultarSessaoUseCase(repo)


def get_atualizar_status_uc(
    sessao_repo: SessaoRepository = Depends(get_sessao_repo),
    ouvinte_repo: OuvinteRepository = Depends(get_ouvinte_repo),
) -> AtualizarStatusSessaoUseCase:
    return AtualizarStatusSessaoUseCase(sessao_repo, ouvinte_repo)
