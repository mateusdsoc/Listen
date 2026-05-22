# Listen — Backend (Sprints 1 e 2)

Backend REST do projeto **Listen**, plataforma que conecta solicitantes de escuta ativa a estudantes de psicologia (ouvintes).

## Stack

- **FastAPI** + **Uvicorn**
- **MongoDB** com **Motor** (driver async)
- **RabbitMQ 3.13** + **aio-pika** (MOM — Sprint 2)
- **Pydantic v2** (entidades de domínio e schemas de I/O)
- **passlib[bcrypt]** para hash de senhas
- **Docker Compose** para subir API + MongoDB + RabbitMQ + Consumer

## Arquitetura (Clean Architecture)

```
app/
├── core/              # config + security (bcrypt)
├── domain/            # entities + repository interfaces + eventos (sem dependências externas)
│   ├── entities/
│   ├── events/        # contrato dos eventos de domínio + porta EventPublisher
│   └── repositories/
├── application/       # use cases (regras de negócio)
│   ├── exceptions.py
│   └── use_cases/
├── infrastructure/    # implementações concretas (Motor/MongoDB, RabbitMQ)
│   ├── database.py
│   ├── messaging/     # conexão, publisher e consumer do RabbitMQ
│   └── repositories/
└── presentation/      # FastAPI: schemas, deps, routers, error handlers
    ├── api/
    │   ├── deps.py
    │   └── v1/
    └── schemas/
```

A regra de dependência aponta sempre para dentro:
`presentation → application → domain` e `infrastructure → domain`.
A camada `domain` não importa nada das outras.

## Como rodar (Docker Compose)

```bash
cd code/backend
docker compose up --build
```

Serviços expostos:

| Serviço | URL / Porta | Observação |
|---------|-------------|------------|
| API | http://localhost:8000 | Swagger em `/docs` |
| MongoDB | `localhost:27017` | Banco `listen` |
| RabbitMQ AMQP | `localhost:5672` | Conexão do backend e do consumer |
| RabbitMQ Management UI | http://localhost:15672 | Login: `guest` / `guest` |
| Consumer | (container `listen-consumer`) | Log em `docker logs -f listen-consumer` |


## Endpoints

Base: `/api/v1`

### Sessões (núcleo da Sprint 1)

| Método | Rota                              | Descrição                                                                |
|--------|-----------------------------------|--------------------------------------------------------------------------|
| POST   | `/sessoes`                        | Solicitante abre uma nova sessão (status inicial = `pendente`)           |
| GET    | `/sessoes/pendentes`              | Lista sessões pendentes (visão do ouvinte)                               |
| GET    | `/sessoes/{id}`                   | Consulta uma sessão por ID (acompanhamento)                              |
| PATCH  | `/sessoes/{id}/status`            | Atualiza o status (aceitar / iniciar / concluir / cancelar)              |

### Cadastros (necessários para suportar o fluxo + hashing de senha)

| Método | Rota               | Descrição                              |
|--------|--------------------|----------------------------------------|
| POST   | `/solicitantes`    | Cadastra um solicitante                |
| POST   | `/ouvintes`        | Cadastra um ouvinte                    |

### Health

| Método | Rota       |
|--------|------------|
| GET    | `/health`  |

## Transições de status válidas

```
pendente     → aceita | cancelada
aceita       → em_andamento | cancelada
em_andamento → concluida | cancelada
concluida    → (terminal)
cancelada    → (terminal)
```

Ao mudar para `aceita`, é obrigatório enviar `ouvinte_id`.

## Coleção de testes

Coleção Postman em [`postman/listen.postman_collection.json`](./postman/listen.postman_collection.json).

## Sprint 2 — Mensageria (RabbitMQ)

O backend publica três eventos de domínio em um **exchange topic**
`listen.events`. O nome do evento é a routing key.

| Evento | Disparado em | Use case |
|--------|-------------|----------|
| `sessao.criada` | criação de sessão (status inicial `pendente`) | `CriarSessaoUseCase` |
| `sessao.aceita` | transição `pendente → aceita` | `AtualizarStatusSessaoUseCase` |
| `sessao.encerrada` | transição para `concluida` ou `cancelada` | `AtualizarStatusSessaoUseCase` |

O container `listen-consumer` faz bind em `sessao.*` na fila
`listen.eventos_log`, grava cada mensagem na coleção `eventos_log` do
Mongo e loga no console — serve como evidência de processamento
assíncrono fora do ciclo HTTP do FastAPI.

Documentação completa: [`docs/sprint2/eventos.md`](../../docs/sprint2/eventos.md)
e [`docs/sprint2/relatorio_integracao.md`](../../docs/sprint2/relatorio_integracao.md).

### Como verificar o fluxo de eventos

```bash
# 1. subir o stack completo
docker compose up --build

# 2. observar o consumer em tempo real (em outro terminal)
docker logs -f listen-consumer

# 3. abrir a UI do RabbitMQ
#    http://localhost:15672  (guest/guest)
#    → Exchanges → listen.events
#    → Queues → listen.eventos_log

# 4. disparar requests pela coleção Postman:
#    - POST /api/v1/sessoes              → emite sessao.criada
#    - PATCH /api/v1/sessoes/{id}/status → emite sessao.aceita ou sessao.encerrada

# 5. inspecionar o histórico no Mongo
docker exec -it listen-mongodb mongosh listen --eval "db.eventos_log.find().pretty()"
```
