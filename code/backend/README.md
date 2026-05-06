# Listen — Backend (Sprint 1)

Backend REST do projeto **Listen**, plataforma que conecta solicitantes de escuta ativa a estudantes de psicologia (ouvintes).

## Stack

- **FastAPI** + **Uvicorn**
- **MongoDB** com **Motor** (driver async)
- **Pydantic v2** (entidades de domínio e schemas de I/O)
- **passlib[bcrypt]** para hash de senhas
- **Docker Compose** para subir API + MongoDB

## Arquitetura (Clean Architecture)

```
app/
├── core/              # config + security (bcrypt)
├── domain/            # entities + repository interfaces (sem dependências externas)
│   ├── entities/
│   └── repositories/
├── application/       # use cases (regras de negócio)
│   ├── exceptions.py
│   └── use_cases/
├── infrastructure/    # Motor/MongoDB - implementações concretas
│   ├── database.py
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

A API ficará em `http://localhost:8000` e o Swagger em `http://localhost:8000/docs`.

MongoDB exposto em `localhost:27017`, banco `listen`.

## Como rodar local (sem Docker)

```bash
cd code/backend
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
copy .env.example .env
# (suba um Mongo local em localhost:27017)
uvicorn app.main:app --reload
```

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

Coleção Postman em [`docs/listen.postman_collection.json`](./docs/listen.postman_collection.json).

## Sprint 2

A integração com **RabbitMQ** (eventos `sessao.criada`, `sessao.aceita`, `sessao.encerrada`) será adicionada na Sprint 2 e **não** está implementada aqui.
