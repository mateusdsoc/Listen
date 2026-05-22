# Roteiro de Coleta de Evidências — Sprint 2

Este roteiro reproduz o fluxo completo de eventos de ponta a ponta e
indica quais screenshots/saídas salvar como evidência da entrega.

## Pré-requisitos

- Docker Desktop rodando.
- Coleção Postman importada (`code/backend/postman/listen.postman_collection.json`).

## 1. Subir o stack

```bash
cd code/backend
docker compose up --build
```

Aguarde até ver as quatro linhas indicando containers prontos:
`listen-mongodb`, `listen-rabbitmq`, `listen-backend`, `listen-consumer`.

**Evidência 01** — `01_compose_up.png`: terminal mostrando os quatro
containers em estado `running`/`healthy`
(`docker compose ps` ou a tela do Docker Desktop).

## 2. RabbitMQ — exchange e fila declarados

Abrir `http://localhost:15672` (login `guest` / `guest`).

- Aba **Exchanges** → confirmar que `listen.events` existe (tipo `topic`,
  durável).
- Aba **Queues** → confirmar que `listen.eventos_log` existe e está
  bindada em `listen.events` com routing key `sessao.*`.

**Evidência 02** — `02_rabbit_exchange.png`: tela do exchange
`listen.events`.
**Evidência 03** — `03_rabbit_queue.png`: tela da fila
`listen.eventos_log` com o binding visível.

## 3. Disparar os três eventos via Postman

Executar na ordem (a coleção encadeia variáveis automaticamente):

1. `0. Health Check`
2. `1. Cadastrar solicitante`
3. `2. Cadastrar ouvinte`
4. `3. Login (solicitante)`
5. `4. Login (ouvinte)`
6. `5. Criar sessão` → produz **`sessao.criada`**
7. `6. Listar sessões pendentes`
8. `7. Consultar sessão por ID`
9. `8. Aceitar sessão` → produz **`sessao.aceita`**
10. `9. Iniciar sessão`
11. `10. Concluir sessão` → produz **`sessao.encerrada`**

**Evidência 04** — `04_postman_fluxo.png`: print do Postman após
executar a sequência (lista de requests com checks verdes).

## 4. Consumer processando assincronamente

Em outro terminal:

```bash
docker logs -f listen-consumer
```

Devem aparecer três linhas começando com `Evento recebido | routing_key=...`
— uma para cada evento publicado no passo 3.

**Evidência 05** — `05_consumer_logs.png`: terminal mostrando os três
eventos consumidos.

## 5. RabbitMQ — contadores de mensagens

Voltar à UI do RabbitMQ → fila `listen.eventos_log` → verificar que o
contador **Total** (Delivered/Get) é maior ou igual a 3.

**Evidência 06** — `06_rabbit_counters.png`: print dos contadores da
fila após o fluxo.

## 6. MongoDB — coleção `eventos_log`

```bash
docker exec -it listen-mongodb mongosh listen --eval "db.eventos_log.find().pretty()"
```

Devem aparecer três documentos: um `sessao.criada`, um `sessao.aceita`
e um `sessao.encerrada` (com `status_final: "concluida"`).

**Evidência 07** — `07_mongo_eventos_log.png`: terminal mostrando os
três documentos.

## Checklist de entrega

- [ ] 7 screenshots em `docs/sprint2/evidencias/`
- [ ] `docs/sprint2/eventos.md` atualizado (catálogo dos eventos)
- [ ] `docs/sprint2/relatorio_integracao.md` (1 página)
- [ ] Coleção Postman com descrição mencionando os eventos
- [ ] README do backend com instruções de Sprint 2
- [ ] Commits separados por bloco no histórico do Git
