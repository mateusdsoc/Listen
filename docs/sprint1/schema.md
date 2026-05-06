# Listen - Schema do MongoDB

## Coleção: solicitantes

| Campo         | Tipo     | Descrição                        |
|---------------|----------|----------------------------------|
| _id           | ObjectId | Identificador único              |
| primeiro_nome | String   | Primeiro nome do solicitante     |
| email         | String   | Email para login                 |
| senha         | String   | Senha (armazenada com hash)      |
| created_at    | DateTime | Data de cadastro                 |

## Coleção: ouvintes

| Campo         | Tipo     | Descrição                              |
|---------------|----------|----------------------------------------|
| _id           | ObjectId | Identificador único                    |
| primeiro_nome | String   | Primeiro nome do ouvinte               |
| email         | String   | Email para login                       |
| senha         | String   | Senha (armazenada com hash)            |
| instituicao   | String   | Instituição de ensino                  |
| periodo       | Int      | Período do curso de psicologia         |
| disponivel    | Boolean  | Se está disponível para atender        |
| created_at    | DateTime | Data de cadastro                       |

## Coleção: sessoes

| Campo           | Tipo     | Descrição                                                 |
|-----------------|----------|-----------------------------------------------------------|
| _id                  | ObjectId | Identificador único                                  |
| solicitante_id       | ObjectId | Referência ao solicitante                            |
| ouvinte_id           | ObjectId | Referência ao ouvinte (null até ser aceita)          |
| descricao            | String   | Descrição do estado emocional do solicitante         |
| status               | String   | pendente, aceita, em_andamento, concluida, cancelada |
| avaliacao            | Object   | Documento embutido (null até ser avaliada)           |
| avaliacao.nota       | Int      | Nota de 1 a 5                                        |
| avaliacao.comentario | String   | Comentário do solicitante sobre a sessão             |
| created_at           | DateTime | Data de criação da sessão                            |
| updated_at           | DateTime | Data da última atualização                           |