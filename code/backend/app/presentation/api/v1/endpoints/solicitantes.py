from fastapi import APIRouter, Depends, status

from app.application.use_cases.criar_solicitante import (
    CriarSolicitanteInput,
    CriarSolicitanteUseCase,
)
from app.presentation.api.deps import get_criar_solicitante_uc
from app.presentation.schemas.solicitante import (
    SolicitanteCreateRequest,
    SolicitanteResponse,
)

router = APIRouter(prefix="/solicitantes", tags=["solicitantes"])


@router.post(
    "",
    response_model=SolicitanteResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastra um novo solicitante",
)
async def criar_solicitante(
    payload: SolicitanteCreateRequest,
    uc: CriarSolicitanteUseCase = Depends(get_criar_solicitante_uc),
) -> SolicitanteResponse:
    entity = await uc.execute(
        CriarSolicitanteInput(
            primeiro_nome=payload.primeiro_nome,
            email=payload.email,
            senha=payload.senha,
        )
    )
    return SolicitanteResponse.from_entity(entity)
