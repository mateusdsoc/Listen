# Arquitetura do App do Cliente — Sprint 3

App **Flutter** do solicitante, organizado em camadas segundo a Clean Architecture
discutida em aula. A regra de dependência aponta sempre para baixo: a UI depende do
estado, que depende dos serviços, que dependem dos modelos.

```
┌─────────────────────────────────────────────────────────────┐
│  screens/            (UI — Widgets)                          │
│  login · cadastro · minhas_sessoes · criar_sessao · detalhe  │
└───────────────┬─────────────────────────────────────────────┘
                │ lê/observa (Provider)
┌───────────────▼─────────────────────────────────────────────┐
│  state/              (ChangeNotifier)                        │
│  AuthProvider · SessoesProvider                              │
└───────────────┬─────────────────────────────────────────────┘
                │ chama
┌───────────────▼─────────────────────────────────────────────┐
│  services/           (regras de acesso à API)               │
│  AuthService · SessaoService  →  ApiClient (http + token)    │
└───────────────┬─────────────────────────────────────────────┘
                │ HTTP REST (JSON)
┌───────────────▼─────────────────────────────────────────────┐
│  Backend FastAPI  /api/v1   (Sprints 1 e 2)                 │
└─────────────────────────────────────────────────────────────┘

models/  → entidades imutáveis (Sessao, StatusSessao, Avaliacao, Usuario)
           usadas em todas as camadas, sem dependências de UI ou HTTP.
core/    → ApiConfig (URL base, intervalo de polling) e ApiException.
widgets/ → componentes de UI reutilizáveis (StatusChip, SessaoCard).
```

## Responsabilidades por camada

| Camada | Responsabilidade | Não faz |
|--------|------------------|---------|
| `models` | Estrutura de dados + (de)serialização JSON | Lógica de rede, estado da UI |
| `core` | Configuração e tipos transversais | Regras de negócio |
| `services` | Montar requisições, anexar token, traduzir erros | Guardar estado, conhecer Widgets |
| `state` | Manter estado observável, orquestrar serviços, polling | Falar HTTP diretamente |
| `widgets` | Componentes visuais sem estado de negócio | Acessar serviços/rede |
| `screens` | Compor a tela e reagir ao estado | Falar HTTP diretamente |

## Endpoints consumidos

| Tela | Método | Endpoint |
|------|--------|----------|
| Cadastro | `POST` | `/solicitantes` |
| Login | `POST` | `/auth/login` (role `solicitante`) |
| Minhas sessões | `GET` | `/sessoes/minhas` |
| Nova sessão | `POST` | `/sessoes` |
| Detalhes | `GET` | `/sessoes/{id}` |
| Detalhes (ações) | `PATCH` | `/sessoes/{id}/status` |

## Atualização assíncrona de estado

Mecanismo escolhido: **polling** (permitido pelo enunciado da Sprint 3).

- `SessoesProvider` dispara um `Timer.periodic` que recarrega `GET /sessoes/minhas` a cada
  5 segundos enquanto a tela de listagem está ativa.
- `DetalheSessaoScreen` mantém um `Timer.periodic` próprio consultando `GET /sessoes/{id}`.

Assim, quando o **ouvinte** aceita uma sessão pelo seu próprio app/fluxo, o backend muda o
status para `aceita` (e publica o evento `sessao.aceita` no RabbitMQ); o app do cliente
detecta a mudança no próximo ciclo de polling e atualiza a interface **sem ação do usuário**.

A integração direta com o MOM (consumir o evento em vez de fazer polling) está planejada
para a Sprint 4.
