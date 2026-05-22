"""Consumer de demonstração para os eventos de sessão.

Executa como processo standalone (independente da API):

    python -m app.infrastructure.messaging.consumers.eventos_consumer

Faz bind na exchange topic `listen.events` com routing key `sessao.*`,
grava cada mensagem na coleção `eventos_log` do Mongo e loga no console.
Serve como evidência de comunicação assíncrona real: o backend publica
sem conhecer o consumer, e este processa fora do ciclo HTTP.
"""
import asyncio
import json
import logging
from datetime import datetime, timezone

import aio_pika
from aio_pika.abc import AbstractIncomingMessage

from app.core.config import settings
from app.infrastructure.database import connect_to_mongo, db
from app.infrastructure.messaging.rabbitmq import (
    broker,
    close_rabbitmq,
    connect_to_rabbitmq,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("eventos_consumer")

ROUTING_PATTERN = "sessao.*"


async def _handle_message(message: AbstractIncomingMessage) -> None:
    async with message.process(requeue=False):
        try:
            payload = json.loads(message.body.decode("utf-8"))
        except json.JSONDecodeError:
            logger.exception("Mensagem com JSON inválido — descartada")
            return

        routing_key = message.routing_key or "<sem-routing-key>"
        logger.info("Evento recebido | routing_key=%s | payload=%s", routing_key, payload)

        if db.database is not None:
            await db.database["eventos_log"].insert_one(
                {
                    "routing_key": routing_key,
                    "evento": payload.get("evento"),
                    "ocorrido_em": payload.get("ocorrido_em"),
                    "data": payload.get("data"),
                    "recebido_em": datetime.now(timezone.utc),
                }
            )


async def main() -> None:
    await connect_to_mongo()
    await connect_to_rabbitmq()

    assert broker.channel is not None and broker.exchange is not None

    queue = await broker.channel.declare_queue(
        settings.rabbitmq_eventos_queue,
        durable=True,
    )
    await queue.bind(broker.exchange, routing_key=ROUTING_PATTERN)

    logger.info(
        "Consumer pronto | fila=%s | bind=%s | exchange=%s",
        settings.rabbitmq_eventos_queue,
        ROUTING_PATTERN,
        settings.rabbitmq_exchange,
    )

    await queue.consume(_handle_message)

    try:
        await asyncio.Future()  # bloqueia até cancelamento
    finally:
        await close_rabbitmq()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Consumer encerrado por sinal.")
