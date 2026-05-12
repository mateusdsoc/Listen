# Arquitetura do Backend — Listen

```
app/
├── main.py                              # entrypoint: cria o FastAPI, conecta ao Mongo, registra rotas
├── core/
│   ├── config.py                        # lê variáveis de ambiente (.env)
│   └── security.py                      # JWT (gerar/decodificar) e hash de senha (bcrypt)
├── domain/                              # regras de negócio puras, sem dependência de framework ou banco
│   ├── entities/
│   │   ├── common.py                    # PyObjectId: converte ObjectId do Mongo para str
│   │   ├── solicitante.py               # entidade Solicitante
│   │   ├── ouvinte.py                   # entidade Ouvinte (+ instituicao, periodo, disponivel)
│   │   └── sessao.py                    # entidade Sessao + enum StatusSessao + Avaliacao
│   └── repositories/                    # interfaces (contratos) que o banco deve implementar
│       ├── solicitante_repository.py
│       ├── ouvinte_repository.py
│       └── sessao_repository.py
├── application/
│   ├── exceptions.py                    # erros de domínio (NotFound, AuthError, EmailDuplicado…)
│   └── use_cases/
│       ├── criar_solicitante.py         # valida email único e persiste
│       ├── criar_ouvinte.py             # idem para ouvinte
│       ├── login.py                     # verifica senha e emite JWT
│       ├── criar_sessao.py              # abre sessão com status pendente
│       ├── listar_sessoes_pendentes.py  # retorna sessões aguardando ouvinte
│       ├── consultar_sessao.py          # busca sessão por ID
│       └── atualizar_status_sessao.py   # valida transição de estado e vincula ouvinte ao aceitar
├── infrastructure/
│   ├── database.py                      # conexão Motor (async) com MongoDB
│   └── repositories/                    # implementações concretas das interfaces do domain
│       ├── mongo_solicitante_repository.py
│       ├── mongo_ouvinte_repository.py
│       └── mongo_sessao_repository.py
└── presentation/
    ├── error_handlers.py                # converte exceções de domínio em respostas HTTP
    ├── schemas/                         # modelos Pydantic de entrada e saída de cada endpoint
    │   ├── auth.py
    │   ├── solicitante.py
    │   ├── ouvinte.py
    │   └── sessao.py
    └── api/v1/
        ├── router.py                    # agrega todos os sub-routers em /api/v1
        ├── deps.py                      # injeção de dependência: instancia repos/use cases, valida JWT
        └── endpoints/
            ├── auth.py                  # POST /auth/login
            ├── solicitantes.py          # POST /solicitantes
            ├── ouvintes.py              # POST /ouvintes
            └── sessoes.py               # POST, GET /pendentes, GET /{id}, PATCH /{id}/status
```
