# Relatório Individual Final - Gabriel Mota - 202302606

## Atribuição de cargo e tarefas:
- Fiquei responsável por auxiliar na documentação do projeto e implementar a camada ORM do sistema.

## Contribuição:
- Desenvolvi com sucesso a base do ORM utilizando inicialmente SQLite, posteriormente migrando para PostgreSQL conforme o planejado. Também implementei as interfaces gráficas em JavaFX e seus respectivos controladores, garantindo a integração completa com o banco de dados relacional.

## Contribuição além do atribuído:
- Além das atividades inicialmente atribuídas, implementei os canais de publicação (publisher) utilizando Redis para viabilizar a comunicação via Pub/Sub. Essa implementação permite que alterações realizadas nas entidades de clientes, produtos e pedidos sejam publicadas de forma assíncrona, possibilitando sua propagação para outros componentes do sistema. O foco da minha contribuição foi *exclusivamente na lógica de publicação dos dados* no Redis. ORM -> ODM

## Considerações gerais:
- A atividade me permitiu aprofundar o conhecimento em ORM, integração com bancos relacionais, uso de JavaFX para construção de interfaces e comunicação assíncrona com Redis.
