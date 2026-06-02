from typing import List

from fastapi import APIRouter, Depends, Path, status

from app.application.use_cases.atualizar_status_sessao import (
    AtualizarStatusSessaoInput,
    AtualizarStatusSessaoUseCase,
)
from app.application.use_cases.consultar_sessao import ConsultarSessaoUseCase
from app.application.use_cases.criar_sessao import (
    CriarSessaoInput,
    CriarSessaoUseCase,
)
from app.application.use_cases.listar_sessoes_do_solicitante import (
    ListarSessoesDoSolicitanteUseCase,
)
from app.application.use_cases.listar_sessoes_pendentes import (
    ListarSessoesPendentesUseCase,
)
from app.presentation.api.deps import (
    CurrentUser,
    get_atualizar_status_uc,
    get_consultar_sessao_uc,
    get_criar_sessao_uc,
    get_current_user,
    get_listar_minhas_sessoes_uc,
    get_listar_pendentes_uc,
)
from app.presentation.schemas.sessao import (
    SessaoCreateRequest,
    SessaoResponse,
    SessaoStatusUpdateRequest,
)

router = APIRouter(prefix="/sessoes", tags=["sessoes"])


@router.post(
    "",
    response_model=SessaoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Solicitante abre uma nova sessão de escuta",
)
async def criar_sessao(
    payload: SessaoCreateRequest,
    current_user: CurrentUser = Depends(get_current_user),
    uc: CriarSessaoUseCase = Depends(get_criar_sessao_uc),
) -> SessaoResponse:
    entity = await uc.execute(
        CriarSessaoInput(
            solicitante_id=current_user.user_id,
            descricao=payload.descricao,
        )
    )
    return SessaoResponse.from_entity(entity)


@router.get(
    "/pendentes",
    response_model=List[SessaoResponse],
    summary="Lista sessões com status pendente para os ouvintes",
)
async def listar_sessoes_pendentes(
    current_user: CurrentUser = Depends(get_current_user),
    uc: ListarSessoesPendentesUseCase = Depends(get_listar_pendentes_uc),
) -> List[SessaoResponse]:
    sessoes = await uc.execute()
    return [SessaoResponse.from_entity(s) for s in sessoes]


@router.get(
    "/minhas",
    response_model=List[SessaoResponse],
    summary="Lista as sessões do solicitante autenticado",
)
async def listar_minhas_sessoes(
    current_user: CurrentUser = Depends(get_current_user),
    uc: ListarSessoesDoSolicitanteUseCase = Depends(get_listar_minhas_sessoes_uc),
) -> List[SessaoResponse]:
    sessoes = await uc.execute(current_user.user_id)
    return [SessaoResponse.from_entity(s) for s in sessoes]


@router.get(
    "/{sessao_id}",
    response_model=SessaoResponse,
    summary="Consulta uma sessão pelo ID",
)
async def consultar_sessao(
    sessao_id: str = Path(..., description="ID da sessão"),
    current_user: CurrentUser = Depends(get_current_user),
    uc: ConsultarSessaoUseCase = Depends(get_consultar_sessao_uc),
) -> SessaoResponse:
    entity = await uc.execute(sessao_id)
    return SessaoResponse.from_entity(entity)


@router.patch(
    "/{sessao_id}/status",
    response_model=SessaoResponse,
    summary="Atualiza o status da sessão (aceitar, iniciar, concluir, cancelar)",
)
async def atualizar_status_sessao(
    payload: SessaoStatusUpdateRequest,
    sessao_id: str = Path(..., description="ID da sessão"),
    current_user: CurrentUser = Depends(get_current_user),
    uc: AtualizarStatusSessaoUseCase = Depends(get_atualizar_status_uc),
) -> SessaoResponse:
    ouvinte_id = payload.ouvinte_id or (
        current_user.user_id if current_user.role == "ouvinte" else None
    )
    entity = await uc.execute(
        AtualizarStatusSessaoInput(
            sessao_id=sessao_id,
            novo_status=payload.status,
            ouvinte_id=ouvinte_id,
        )
    )
    return SessaoResponse.from_entity(entity)
