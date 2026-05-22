from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class EventoDominio:
    """Evento de domínio publicado no MOM.

    `nome` corresponde à routing key usada no exchange topic.
    `payload` é o conteúdo serializável (dict) que será publicado como JSON.
    """

    nome: str
    payload: dict[str, Any]
    ocorrido_em: str = field(default_factory=_now_iso)

def sessao_criada(
    sessao_id: str,
    solicitante_id: str,
    descricao: str,
) -> EventoDominio:
    return EventoDominio(
        nome="sessao.criada",
        payload={
            "sessao_id": sessao_id,
            "solicitante_id": solicitante_id,
            "descricao": descricao,
        },
    )


def sessao_aceita(
    sessao_id: str,
    solicitante_id: str,
    ouvinte_id: str,
) -> EventoDominio:
    return EventoDominio(
        nome="sessao.aceita",
        payload={
            "sessao_id": sessao_id,
            "solicitante_id": solicitante_id,
            "ouvinte_id": ouvinte_id,
        },
    )


def sessao_encerrada(
    sessao_id: str,
    solicitante_id: str,
    ouvinte_id: Optional[str],
    status_final: str,
) -> EventoDominio:
    return EventoDominio(
        nome="sessao.encerrada",
        payload={
            "sessao_id": sessao_id,
            "solicitante_id": solicitante_id,
            "ouvinte_id": ouvinte_id,
            "status_final": status_final,
        },
    )
