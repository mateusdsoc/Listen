# Relatório de Integração — Sprint 2

**Projeto:** Listen — plataforma de escuta ativa
**Sprint:** 2 (Integração com Middleware Orientado a Mensagens)
**Data:** 25/05/2026

## 1. Escolha da ferramenta

Para o MOM foi adotado o **RabbitMQ 3.13** com o plugin de gerenciamento.
A decisão considerou três alternativas (RabbitMQ, Redis Pub/Sub e
Apache Kafka):

- **RabbitMQ** implementa diretamente os padrões descritos em Hohpe &
  Woolf (*Enterprise Integration Patterns*), referência oficial da
  ementa. Exchanges, filas, bindings e *durable messages* mapeiam 1-para-1
  com o vocabulário do livro, o que torna o projeto pedagogicamente
  alinhado.
- **Redis Pub/Sub** é mais simples, porém não persiste mensagens: um
  consumer offline perde tudo. Para um domínio em que o ouvinte pode
  estar com o app fechado, isso é uma limitação real.
- **Kafka** seria sobre-engenharia para o volume e o escopo do projeto.

A UI de gerenciamento (porta `15672`) também ajuda na entrega da sprint:
permite mostrar visualmente o exchange, a fila e o tráfego de mensagens.

## 2. Padrão arquitetural

Foi adotado um **exchange topic** chamado `listen.events`. O nome do
evento é usado como routing key (`sessao.criada`, `sessao.aceita`,
`sessao.encerrada`), o que permite que consumers façam bind tanto por
evento específico quanto por padrão (`sessao.*`). Esse padrão segue a
recomendação de *publish-subscribe channel* com *content-based routing*
de Hohpe & Woolf e antecipa o cenário da Sprint 4, em que o app do
solicitante consumirá apenas eventos relativos à sua sessão e o app do
ouvinte consumirá apenas `sessao.criada`.

O envelope das mensagens é padronizado (`evento`, `ocorrido_em`, `data`),
o que evita acoplamento entre produtor e consumer ao identificar o tipo
de mensagem — qualquer consumer pode decidir o que fazer baseado no
campo `evento`, sem inspecionar a routing key.

## 3. Decisões de design

**Publisher como porta do domínio.** A interface `EventPublisher` vive
em `domain/events/publisher.py` como `Protocol`. A implementação concreta
`RabbitMQEventPublisher` está em `infrastructure/messaging/`. Os use
cases recebem o publisher por injeção, mantendo a Clean Architecture e
permitindo testes com um *fake publisher* sem subir RabbitMQ.

**Publicação após a persistência.** Cada use case persiste no Mongo
**antes** de publicar. Assim, se a publicação falhar, o estado do
sistema continua consistente (a sessão existe e pode ser reprocessada
posteriormente). É a heurística de *outbox simplificado*: aceita-se a
possibilidade rara de uma escrita sem evento, mas nunca um evento sem
escrita.

**Consumer em processo separado.** O `eventos_consumer.py` roda como
container independente (`listen-consumer`). O backend publica no exchange
sem nenhuma chamada direta ao consumer; o consumer processa as mensagens
fora do ciclo HTTP e grava cada uma na coleção `eventos_log` do Mongo.

## 4. Desafios encontrados

- **Ordem de inicialização**: o backend pode subir antes do RabbitMQ
  estar pronto para aceitar conexões mesmo com `depends_on`. Foi
  implementada uma estratégia de *retry* com 10 tentativas em
  `connect_to_rabbitmq`, evitando *crash loop* do container.
- **Conexão robusta**: usou-se `connect_robust` do `aio-pika`, que
  reconecta automaticamente caso o broker reinicie, evitando que uma
  queda momentânea derrube o backend.
## 5. Evidências de funcionamento

O fluxo completo foi executado em 25/05/2026 via Postman, na seguinte
sequência: cadastro de solicitante e ouvinte, login dos dois, criação de
sessão, aceite, início e conclusão.

**RabbitMQ — exchange** (`rabbit_exchanges.png`): a aba Exchanges da UI
de gerenciamento (porta `15672`) exibiu o exchange `listen.events` do
tipo `topic`, com a flag `D` (durable), confirmando que o exchange
persiste reinicializações do broker.

**RabbitMQ — fila e binding** (`rabbit_fila.png`): no detalhe da fila
`listen.eventos_log` foi visível o binding `sessao.*` originado do
exchange `listen.events`, confirmando que qualquer evento com routing key
prefixada por `sessao.` é entregue à fila.

**Logs do consumer** (`consumer_logs.png`): ao subir, o container
`listen-consumer` registrou uma falha de conexão na tentativa 1/10 (o
RabbitMQ ainda estava inicializando), reconectou automaticamente e
anunciou `Consumer pronto | fila=listen.eventos_log | bind=sessao.*`.
Após a execução do fluxo, os três eventos foram recebidos em ordem:
`sessao.criada` (22:17:44), `sessao.aceita` (22:18:09) e
`sessao.encerrada` (22:18:18) com `status_final: concluida`.

**MongoDB** (`mongo_eventos.png`): o comando
`db.eventos_log.find().pretty()` retornou exatamente três documentos,
um para cada evento, com os campos `routing_key`, `evento`, `ocorrido_em`,
`data` e `recebido_em` preenchidos corretamente e coerentes com os
timestamps dos logs do consumer.
