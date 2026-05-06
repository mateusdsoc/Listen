from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

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


def get_db() -> AsyncIOMotorDatabase:
    return get_database()


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


def get_criar_solicitante_uc(
    repo: SolicitanteRepository = Depends(get_solicitante_repo),
) -> CriarSolicitanteUseCase:
    return CriarSolicitanteUseCase(repo)


def get_criar_ouvinte_uc(
    repo: OuvinteRepository = Depends(get_ouvinte_repo),
) -> CriarOuvinteUseCase:
    return CriarOuvinteUseCase(repo)


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
