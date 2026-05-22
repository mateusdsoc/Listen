from typing import Protocol

from .eventos_sessao import EventoDominio


class EventPublisher(Protocol):
    """Porta de saída: publica eventos de domínio em um MOM.

    Implementação concreta vive em `infrastructure/messaging`, mantendo o
    domínio livre de dependências do RabbitMQ.
    """

    async def publish(self, evento: EventoDominio) -> None: ...
