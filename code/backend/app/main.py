from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.infrastructure.database import close_mongo_connection, connect_to_mongo
from app.infrastructure.messaging.rabbitmq import close_rabbitmq, connect_to_rabbitmq
from app.presentation.api.v1.router import api_router
from app.presentation.error_handlers import register_exception_handlers


@asynccontextmanager
async def lifespan(_: FastAPI):
    await connect_to_mongo()
    await connect_to_rabbitmq()
    yield
    await close_rabbitmq()
    await close_mongo_connection()


app = FastAPI(
    title=settings.project_name,
    version="0.1.0",
    lifespan=lifespan,
)

register_exception_handlers(app)
app.include_router(api_router, prefix=settings.api_v1_prefix)


@app.get("/health", tags=["health"])
async def health() -> dict:
    return {"status": "ok"}
