# 🐳 Executando MongoDB e Redis com Docker Compose

Este projeto utiliza **Docker Compose** para iniciar instâncias locais do **MongoDB** e do **Redis**, facilitando testes e o desenvolvimento.

---

## 🔹 Subir os serviços

Para iniciar os containers do MongoDB e Redis em segundo plano:

```bash
docker-compose up -d
```

---

## 🔹 Verificar o status dos containers

Para visualizar os containers em execução e conferir o estado dos serviços:

```bash
docker-compose ps
```

---

## 🔹 Ativar o terminal do redis

```bash
docker exec -it redis redis-cli
```

---

## 🔹 Finalizar os serviços

Para parar os containers e remover todos os recursos criados:

```bash
docker-compose down
```
