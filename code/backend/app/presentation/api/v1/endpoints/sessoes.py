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
from app.application.use_cases.listar_sessoes_pendentes import (
    ListarSessoesPendentesUseCase,
)
from app.presentation.api.deps import (
    get_atualizar_status_uc,
    get_consultar_sessao_uc,
    get_criar_sessao_uc,
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
    uc: CriarSessaoUseCase = Depends(get_criar_sessao_uc),
) -> SessaoResponse:
    entity = await uc.execute(
        CriarSessaoInput(
            solicitante_id=payload.solicitante_id,
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
    uc: ListarSessoesPendentesUseCase = Depends(get_listar_pendentes_uc),
) -> List[SessaoResponse]:
    sessoes = await uc.execute()
    return [SessaoResponse.from_entity(s) for s in sessoes]


@router.get(
    "/{sessao_id}",
    response_model=SessaoResponse,
    summary="Consulta uma sessão pelo ID",
)
async def consultar_sessao(
    sessao_id: str = Path(..., description="ID da sessão"),
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
    uc: AtualizarStatusSessaoUseCase = Depends(get_atualizar_status_uc),
) -> SessaoResponse:
    entity = await uc.execute(
        AtualizarStatusSessaoInput(
            sessao_id=sessao_id,
            novo_status=payload.status,
            ouvinte_id=payload.ouvinte_id,
        )
    )
    return SessaoResponse.from_entity(entity)
