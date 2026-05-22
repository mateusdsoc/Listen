import json
import logging

import aio_pika

from app.domain.events.eventos_sessao import EventoDominio
from app.domain.events.publisher import EventPublisher

from .rabbitmq import get_exchange

logger = logging.getLogger(__name__)


class RabbitMQEventPublisher(EventPublisher):
    """Publica eventos de domínio no exchange topic do RabbitMQ.

    O `nome` do evento é usado como routing key, permitindo que consumers
    façam bind com padrões como `sessao.*` ou eventos específicos.
    """

    async def publish(self, evento: EventoDominio) -> None:
        body = json.dumps(
            {
                "evento": evento.nome,
                "ocorrido_em": evento.ocorrido_em,
                "data": evento.payload,
            }
        ).encode("utf-8")

        message = aio_pika.Message(
            body=body,
            content_type="application/json",
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
        )

        exchange = get_exchange()
        await exchange.publish(message, routing_key=evento.nome)
        logger.info("Evento publicado | routing_key=%s", evento.nome)
