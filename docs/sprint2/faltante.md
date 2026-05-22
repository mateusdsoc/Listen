# O que ainda falta fazer

## Tirar os screenshots de evidência

Antes de entregar a Sprint 2, você precisa subir o stack e executar o
fluxo completo uma vez para gerar as evidências. Os prints devem ficar
em `docs/sprint2/evidencias/`.

**Para subir tudo:**
```bash
cd code/backend
docker compose up --build
```

**Fluxo a executar no Postman** (na ordem da coleção):
cadastrar solicitante → cadastrar ouvinte → login dos dois → criar
sessão → aceitar → iniciar → concluir.

**O que printar:**

1. A tela do RabbitMQ em `http://localhost:15672` mostrando o exchange
   `listen.events` (aba Exchanges).
2. A mesma UI mostrando a fila `listen.eventos_log` com o binding
   `sessao.*` visível (aba Queues).
3. O terminal com `docker logs -f listen-consumer` depois de executar
   o fluxo — tem que aparecer os três eventos sendo consumidos.
4. O resultado do comando abaixo, mostrando os três documentos gravados
   no Mongo:
   ```bash
   docker exec -it listen-mongodb mongosh listen --eval "db.eventos_log.find().pretty()"
   ```

Quatro prints são suficientes. Salve com nomes que façam sentido, tipo
`rabbit_exchange.png`, `rabbit_fila.png`, `consumer_logs.png`,
`mongo_eventos.png`.

## Atualizar a seção 5 do relatório

Depois de tirar os prints, reescreva o final da seção 5 do
`relatorio_integracao.md` descrevendo o que você viu — no passado,
como se estivesse relatando o que aconteceu.
