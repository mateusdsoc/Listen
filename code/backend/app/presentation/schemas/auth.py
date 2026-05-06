from pydantic import BaseModel, EmailStr, Field

from app.application.use_cases.login import Role


class LoginRequest(BaseModel):
    email: EmailStr
    senha: str = Field(min_length=1)
    role: Role


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    nome: str
    email: str
    role: str
