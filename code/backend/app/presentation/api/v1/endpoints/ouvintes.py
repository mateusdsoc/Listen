from fastapi import APIRouter, Depends, status

from app.application.use_cases.criar_ouvinte import (
    CriarOuvinteInput,
    CriarOuvinteUseCase,
)
from app.presentation.api.deps import get_criar_ouvinte_uc
from app.presentation.schemas.ouvinte import OuvinteCreateRequest, OuvinteResponse

router = APIRouter(prefix="/ouvintes", tags=["ouvintes"])


@router.post(
    "",
    response_model=OuvinteResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastra um novo ouvinte (estudante de psicologia)",
)
async def criar_ouvinte(
    payload: OuvinteCreateRequest,
    uc: CriarOuvinteUseCase = Depends(get_criar_ouvinte_uc),
) -> OuvinteResponse:
    entity = await uc.execute(
        CriarOuvinteInput(
            primeiro_nome=payload.primeiro_nome,
            email=payload.email,
            senha=payload.senha,
            instituicao=payload.instituicao,
            periodo=payload.periodo,
            disponivel=payload.disponivel,
        )
    )
    return OuvinteResponse.from_entity(entity)
