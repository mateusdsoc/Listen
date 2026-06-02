# Listen — App do Cliente (Sprint 3)

Aplicativo **Flutter** do **solicitante** (cliente) da plataforma Listen. Permite cadastrar-se,
autenticar, abrir sessões de escuta e acompanhar o atendimento. Reflete automaticamente
mudanças de estado do servidor (ex.: quando um ouvinte aceita a sessão) via **polling**.

## Stack

- **Flutter / Dart**
- **provider** — gerenciamento de estado (Clean Architecture)
- **http** — consumo do backend REST

## Arquitetura (camadas)

```
lib/
├── core/         # configuração (URL base, intervalo de polling) e exceção da API
├── models/       # entidades imutáveis espelhando o backend (Sessao, StatusSessao, ...)
├── services/     # ApiClient (HTTP + token) + AuthService + SessaoService
├── state/        # ChangeNotifiers (AuthProvider, SessoesProvider) — estado da UI
├── widgets/      # componentes reutilizáveis (StatusChip, SessaoCard)
├── screens/      # telas (login, cadastro, listagem, criação, detalhe)
└── main.dart     # composição: instancia serviços e registra os providers
```

Fluxo de dependência: `screens → state → services → models`. As telas nunca falam HTTP
diretamente; passam pelos providers e serviços.

## Telas

1. **Login / Cadastro** — autenticação do solicitante (`POST /auth/login`, `POST /solicitantes`).
2. **Minhas sessões** (listagem) — `GET /sessoes/minhas`, com pull-to-refresh e polling.
3. **Nova sessão** (ação principal) — `POST /sessoes`.
4. **Detalhes da sessão** — `GET /sessoes/{id}` com polling; ações de concluir/cancelar
   (`PATCH /sessoes/{id}/status`).

## Atualização assíncrona de estado

O app não exige ação manual para refletir o servidor:

- A lista "minhas sessões" recarrega a cada `ApiConfig.pollingInterval` (5s).
- A tela de detalhes consulta a sessão no mesmo intervalo — quando o ouvinte aceita
  (evento `sessao.aceita` no backend), o status muda de *Aguardando ouvinte* para *Aceita*
  sozinho.

A integração direta com o MOM fica para a Sprint 4; nesta sprint o enunciado permite polling.

## Como rodar

Pré-requisitos: backend no ar (`cd code/backend && docker compose up --build`).

```bash
cd code/app_cliente
flutter pub get
flutter run            # escolha o dispositivo (emulador Android ou Chrome)
```

URL base da API (em `lib/core/api_config.dart`):

| Alvo | URL usada |
|------|-----------|
| Flutter Web (Chrome) | `http://localhost:8000` |
| Emulador Android | `http://10.0.2.2:8000` |
| Dispositivo físico | troque por `http://<ip-da-maquina>:8000` |

## Testes

```bash
flutter analyze
flutter test
```
