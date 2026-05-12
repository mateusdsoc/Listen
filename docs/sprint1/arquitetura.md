# Arquitetura do Backend — Listen

## Estrutura de pastas e arquivos

```
app/
├── main.py
├── core/
│   ├── config.py
│   └── security.py
├── domain/
│   ├── entities/
│   │   ├── common.py
│   │   ├── solicitante.py
│   │   ├── ouvinte.py
│   │   └── sessao.py
│   └── repositories/
│       ├── solicitante_repository.py
│       ├── ouvinte_repository.py
│       └── sessao_repository.py
├── application/
│   ├── exceptions.py
│   └── use_cases/
│       ├── criar_solicitante.py
│       ├── criar_ouvinte.py
│       ├── login.py
│       ├── criar_sessao.py
│       ├── listar_sessoes_pendentes.py
│       ├── consultar_sessao.py
│       └── atualizar_status_sessao.py
├── infrastructure/
│   ├── database.py
│   └── repositories/
│       ├── mongo_solicitante_repository.py
│       ├── mongo_ouvinte_repository.py
│       └── mongo_sessao_repository.py
└── presentation/
    ├── error_handlers.py
    ├── schemas/
    │   ├── auth.py
    │   ├── solicitante.py
    │   ├── ouvinte.py
    │   └── sessao.py
    └── api/v1/
        ├── router.py
        ├── deps.py
        └── endpoints/
            ├── auth.py
            ├── solicitantes.py
            ├── ouvintes.py
            └── sessoes.py
```

---

## Descrição por camada

### `main.py`
Ponto de entrada da aplicação. Cria o app FastAPI, registra os error handlers e conecta/desconecta do MongoDB via lifespan.

---

### `core/`
Utilitários transversais sem regra de negócio.

| Arquivo | Responsabilidade |
|---------|-----------------|
| `config.py` | Lê variáveis de ambiente (`.env`) via Pydantic Settings — URI do Mongo, nome do banco, segredo JWT, expiração do token |
| `security.py` | Geração e decodificação de tokens JWT; hash e verificação de senha com bcrypt |

---

### `domain/`
Núcleo da aplicação. Não importa nada de banco de dados ou framework — apenas Python puro e Pydantic.

#### `domain/entities/`

| Arquivo | Campos principais |
|---------|------------------|
| `common.py` | `PyObjectId` — converte o `ObjectId` do MongoDB para `str` nos modelos |
| `solicitante.py` | `id`, `primeiro_nome`, `email`, `senha`, `created_at` |
| `ouvinte.py` | Herda campos do solicitante + `instituicao`, `periodo` (1–12), `disponivel` |
| `sessao.py` | `id`, `solicitante_id`, `ouvinte_id`, `descricao`, `status` (enum), `avaliacao`, `created_at`, `updated_at` |

Status possíveis da sessão (`StatusSessao`): `pendente`, `aceita`, `em_andamento`, `concluida`, `cancelada`.

#### `domain/repositories/`
Interfaces (classes abstratas) que definem o contrato que qualquer implementação de banco deve cumprir. A camada de `application` depende apenas dessas interfaces, nunca do Mongo diretamente.

---

### `application/`
Casos de uso — orquestram as regras de negócio usando as interfaces de repositório.

| Arquivo | O que faz |
|---------|-----------|
| `exceptions.py` | Erros de domínio: `NotFoundError`, `AuthenticationError`, `EmailDuplicadoError`, `InvalidStateTransitionError`, `ValidationError` |
| `criar_solicitante.py` | Valida que o email não existe nem em solicitantes nem em ouvintes; persiste com senha em hash |
| `criar_ouvinte.py` | Igual ao acima, para ouvintes |
| `login.py` | Busca o usuário pela role informada, verifica a senha, emite JWT com `sub` (user_id) e `role` |
| `criar_sessao.py` | Cria sessão com status `pendente` vinculada ao solicitante autenticado |
| `listar_sessoes_pendentes.py` | Retorna todas as sessões com status `pendente` |
| `consultar_sessao.py` | Busca uma sessão pelo ID |
| `atualizar_status_sessao.py` | Valida a transição de estado segundo a máquina abaixo; ao aceitar, vincula o `ouvinte_id` |

Máquina de estados das sessões:
```
pendente → aceita | cancelada
aceita → em_andamento | cancelada
em_andamento → concluida | cancelada
concluida → (terminal)
cancelada → (terminal)
```

---

### `infrastructure/`
Implementações concretas do banco de dados.

| Arquivo | Responsabilidade |
|---------|-----------------|
| `database.py` | Abre e fecha a conexão com MongoDB via Motor (async); expõe `get_database()` |
| `mongo_solicitante_repository.py` | Implementa a interface `SolicitanteRepository` usando Motor |
| `mongo_ouvinte_repository.py` | Implementa `OuvinteRepository` |
| `mongo_sessao_repository.py` | Implementa `SessaoRepository` (inclui `update_status` e `list_by_status`) |

---

### `presentation/`
Camada HTTP — o que o mundo externo enxerga.

| Arquivo/Pasta | Responsabilidade |
|---------------|-----------------|
| `error_handlers.py` | Converte exceções de domínio em respostas HTTP (`404`, `401`, `409`, `422`, `400`) |
| `schemas/auth.py` | `LoginRequest` (email, senha, role) / `LoginResponse` (token, user_id, nome, role) |
| `schemas/solicitante.py` | `SolicitanteCreateRequest` / `SolicitanteResponse` |
| `schemas/ouvinte.py` | `OuvinteCreateRequest` / `OuvinteResponse` |
| `schemas/sessao.py` | `SessaoCreateRequest`, `SessaoStatusUpdateRequest`, `SessaoResponse` |
| `api/v1/router.py` | Agrega todos os sub-routers sob o prefixo `/api/v1` |
| `api/v1/deps.py` | Injeção de dependência: instancia repositórios e casos de uso; valida JWT e expõe `CurrentUser` |
| `api/v1/endpoints/auth.py` | `POST /auth/login` |
| `api/v1/endpoints/solicitantes.py` | `POST /solicitantes` |
| `api/v1/endpoints/ouvintes.py` | `POST /ouvintes` |
| `api/v1/endpoints/sessoes.py` | `POST /sessoes`, `GET /sessoes/pendentes`, `GET /sessoes/{id}`, `PATCH /sessoes/{id}/status` |

---

## O que ainda não está implementado

| Funcionalidade | Existe na entidade? | Tem endpoint? |
|---------------|--------------------|-|
| Avaliação da sessão (nota 1–5 + comentário) | Sim (`Sessao.avaliacao`) | Não |
| Perfil do usuário logado | — | Não |
| Atualizar disponibilidade do ouvinte | Sim (`Ouvinte.disponivel`) | Não |
| Listar sessões do solicitante | — | Não |
| Eventos via RabbitMQ (Sprint 2) | — | Não |
