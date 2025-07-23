# 🐳 Como rodar o MongoDB com Docker Compose

Este projeto utiliza **Docker Compose** para executar uma instância local do MongoDB voltada aos testes e ao desenvolvimento.

## 🔹 Iniciar o MongoDB

Para subir o serviço do MongoDB em segundo plano:

```bash
docker-compose up -d
```

## 🔹 Verificar o status dos containers

Para listar todos os containers em execução e verificar o estado do MongoDB:

```bash
docker-compose ps
```

## 🔹 Encerrar o MongoDB

Para parar e remover os containers criados:

```bash
docker-compose down
```
