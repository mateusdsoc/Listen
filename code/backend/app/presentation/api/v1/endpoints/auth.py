from fastapi import APIRouter, Depends

from app.application.use_cases.login import LoginInput, LoginUseCase
from app.presentation.api.deps import get_login_uc
from app.presentation.schemas.auth import LoginRequest, LoginResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/login",
    response_model=LoginResponse,
    summary="Autentica solicitante ou ouvinte e retorna JWT",
)
async def login(
    payload: LoginRequest,
    uc: LoginUseCase = Depends(get_login_uc),
) -> LoginResponse:
    result = await uc.execute(
        LoginInput(
            email=payload.email,
            senha=payload.senha,
            role=payload.role,
        )
    )
    return LoginResponse(
        access_token=result.access_token,
        token_type=result.token_type,
        user_id=result.user_id,
        nome=result.nome,
        email=result.email,
        role=result.role,
    )
