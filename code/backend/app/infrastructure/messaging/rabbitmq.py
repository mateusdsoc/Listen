import asyncio
import logging
from typing import Optional

import aio_pika
from aio_pika.abc import AbstractRobustChannel, AbstractRobustConnection, AbstractRobustExchange

from app.core.config import settings

logger = logging.getLogger(__name__)


class RabbitMQ:
    connection: Optional[AbstractRobustConnection] = None
    channel: Optional[AbstractRobustChannel] = None
    exchange: Optional[AbstractRobustExchange] = None


broker = RabbitMQ()


async def connect_to_rabbitmq(retries: int = 10, delay_seconds: float = 2.0) -> None:
    """Estabelece conexão robusta com o RabbitMQ e declara o exchange topic.

    Tenta múltiplas vezes porque o container pode demorar a ficar pronto
    mesmo após o healthcheck (em ambientes locais sem compose).
    """
    last_error: Optional[Exception] = None
    for attempt in range(1, retries + 1):
        try:
            broker.connection = await aio_pika.connect_robust(settings.rabbitmq_url)
            broker.channel = await broker.connection.channel()
            broker.exchange = await broker.channel.declare_exchange(
                settings.rabbitmq_exchange,
                aio_pika.ExchangeType.TOPIC,
                durable=True,
            )
            logger.info(
                "RabbitMQ conectado | exchange=%s", settings.rabbitmq_exchange
            )
            return
        except Exception as exc:  # noqa: BLE001
            last_error = exc
            logger.warning(
                "Falha ao conectar no RabbitMQ (tentativa %s/%s): %s",
                attempt,
                retries,
                exc,
            )
            await asyncio.sleep(delay_seconds)
    raise RuntimeError(f"Não foi possível conectar ao RabbitMQ: {last_error}")


async def close_rabbitmq() -> None:
    if broker.connection is not None and not broker.connection.is_closed:
        await broker.connection.close()


def get_exchange() -> AbstractRobustExchange:
    if broker.exchange is None:
        raise RuntimeError("RabbitMQ não foi inicializado")
    return broker.exchange
