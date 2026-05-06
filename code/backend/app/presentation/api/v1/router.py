from fastapi import APIRouter

from app.presentation.api.v1.endpoints import ouvintes, sessoes, solicitantes

api_router = APIRouter()
api_router.include_router(solicitantes.router)
api_router.include_router(ouvintes.router)
api_router.include_router(sessoes.router)
