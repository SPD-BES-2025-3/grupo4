# E-commerce - Sistema de Persistência de Dados - Grupo 4

## Visão Geral

Este projeto implementa um sistema de e-commerce completo com arquitetura distribuída, integrando múltiplas tecnologias para demonstrar diferentes abordagens de persistência de dados e comunicação entre sistemas. O projeto é composto por uma aplicação desktop Java (CRM) e um backend Python (API REST), com sincronização em tempo real via Redis.

## Arquitetura do Sistema

### Componentes Principais

1. **Aplicação Desktop Java (CRM)**
   - Interface gráfica JavaFX
   - Persistência PostgreSQL via ORMLite
   - Gerenciamento de produtos, clientes e pedidos
   - Publicação de eventos via Redis

2. **Backend Python (API REST)**
   - API FastAPI para operações de e-commerce
   - Persistência MongoDB via Beanie ODM
   - Receptor de eventos Redis
   - Sincronização automática de dados

3. **Sistema de Mensageria**
   - Redis como message broker
   - Comunicação assíncrona entre componentes
   - Sincronização em tempo real

### Fluxo de Dados

```
Java (PostgreSQL) → Redis → Python → MongoDB
```

## Tecnologias Utilizadas

### Backend Java (CRM)
- **Java 21** - Linguagem principal
- **JavaFX** - Interface gráfica desktop
- **ORMLite** - ORM para PostgreSQL
- **PostgreSQL** - Banco de dados relacional
- **Maven** - Gerenciamento de dependências
- **JUnit 4** - Testes unitários
- **Mockito** - Framework de mocking

### Backend Python (API)
- **Python 3.12** - Linguagem principal
- **FastAPI** - Framework web para APIs
- **Beanie** - ODM para MongoDB
- **Motor** - Driver assíncrono MongoDB
- **Redis-py** - Cliente Redis Python
- **Pytest** - Framework de testes
- **Uvicorn** - Servidor ASGI

### Infraestrutura
- **Redis** - Message broker e cache
- **MongoDB** - Banco de dados NoSQL
- **PostgreSQL** - Banco de dados relacional
- **Docker** - Containerização
- **Docker Compose** - Orquestração de containers

## Estrutura do Projeto

```
grupo4/
├── orm/                          # Aplicação Java (CRM)
│   ├── src/main/java/
│   │   ├── com/exemplo/hello/
│   │   │   ├── controller/       # Controladores JavaFX
│   │   │   ├── model/           # Entidades de domínio
│   │   │   ├── redis/           # Publicadores Redis
│   │   │   └── view/            # Views JavaFX
│   │   └── resources/
│   │       └── view/            # Arquivos FXML
│   ├── src/test/java/           # Testes unitários Java
│   ├── pom.xml                  # Dependências Maven
│   └── docker-compose.yml       # Configuração Docker
├── src/main/python/             # Backend Python (API)
│   ├── api/                     # Rotas FastAPI
│   ├── models/                  # Modelos Beanie
│   ├── services/                # Lógica de negócio
│   ├── repositories/            # Acesso a dados
│   ├── config/                  # Configurações
│   ├── testes/                  # Testes Python
│   ├── redis_receiver_final.py  # Receptor Redis principal
│   ├── start_system.sh         # Script de inicialização
│   ├── test_system.sh          # Script de teste
│   └── requirements.txt         # Dependências Python
├── docs/                        # Documentação e diagramas
├── db/                          # Scripts de banco de dados
└── README.md                    # Este arquivo
```

## Funcionalidades Implementadas

### Aplicação Java (CRM)
- **Gerenciamento de Produtos**: CRUD completo com interface gráfica
- **Gerenciamento de Clientes**: Cadastro e consulta de clientes
- **Gerenciamento de Pedidos**: Processamento de pedidos
- **Carrinho de Compras**: Adição e remoção de produtos
- **Publicação de Eventos**: Sincronização via Redis
- **Interface Gráfica**: JavaFX com FXML

### Backend Python (API)
- **API REST**: Endpoints para produtos, clientes, pedidos
- **Receptor Redis**: Sincronização em tempo real
- **Persistência MongoDB**: Armazenamento de dados
- **Validação de Dados**: Pydantic models
- **Testes Automatizados**: Pytest

### Sistema de Sincronização
- **Comunicação Assíncrona**: Redis Pub/Sub
- **Sincronização Automática**: Java → Python → MongoDB
- **Tratamento de Eventos**: CREATE, UPDATE, DELETE
- **Logs Detalhados**: Monitoramento de operações

## Como Executar

### Pré-requisitos

1. **Java 21** instalado
2. **Python 3.12** instalado
3. **Docker** e **Docker Compose** instalados
4. **Git** instalado

### Instalação e Configuração

#### 1. Clonar o Repositório
```bash
git clone https://github.com/SPD-BES-2025-3/grupo4.git
cd grupo4
```

#### 2. Configurar Banco de Dados
```bash
# Iniciar PostgreSQL e MongoDB via Docker
docker-compose up -d

# Verificar se os serviços estão rodando
docker ps
```

#### 3. Configurar Aplicação Java
```bash
cd orm
mvn clean install
```

#### 4. Configurar Backend Python
```bash
cd src/main/python
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Execução do Sistema

#### Opção 1: Inicialização Automática (Recomendada)
```bash
cd src/main/python
./start_system.sh
```

#### Opção 2: Inicialização Manual

1. **Iniciar Receptor Python**
```bash
cd src/main/python
source venv/bin/activate
python redis_receiver_final.py
```

2. **Executar Aplicação Java**
```bash
cd orm
mvn javafx:run
```

3. **Testar Sistema**
```bash
cd src/main/python
./test_system.sh
```

### Verificação do Sistema

#### Verificar Status dos Serviços
```bash
# Verificar se o receptor Python está rodando
ps aux | grep redis_receiver_final

# Verificar produtos no MongoDB
mongosh --eval "use ecommerce; db.produtos.find().pretty()"

# Verificar conexão Redis
redis-cli ping
```

#### Testar Funcionalidades
1. **Criar Produto no Java**: Use a interface gráfica para adicionar produtos
2. **Verificar Sincronização**: Observe os logs do Python
3. **Consultar MongoDB**: Verifique se os dados foram salvos

## Testes

### Testes Java
```bash
cd orm
mvn test
```

### Testes Python
```bash
cd src/main/python
source venv/bin/activate
pytest
```

### Teste de Integração
```bash
cd src/main/python
./test_system.sh
```

## Monitoramento e Logs

### Logs do Sistema
- **Java**: Logs no console da aplicação
- **Python**: Logs detalhados no console do receptor
- **Redis**: Monitoramento via `redis-cli monitor`
- **MongoDB**: Logs via `docker logs <container_id>`

### Comandos de Monitoramento
```bash
# Verificar processos ativos
ps aux | grep -E "(redis_receiver|java|python)"

# Monitorar Redis
redis-cli monitor

# Verificar dados MongoDB
mongosh --eval "use ecommerce; db.produtos.countDocuments()"
```

## Troubleshooting

### Problemas Comuns

#### 1. Redis não conecta
```bash
# Verificar se Redis está rodando
redis-cli ping

# Iniciar Redis manualmente
redis-server --daemonize yes
```

#### 2. MongoDB não conecta
```bash
# Verificar container Docker
docker ps | grep mongo

# Reiniciar container
docker restart <container_id>
```

#### 3. Receptor Python não recebe mensagens
```bash
# Verificar se está rodando
ps aux | grep redis_receiver_final

# Reiniciar receptor
pkill -f redis_receiver_final.py
cd src/main/python && source venv/bin/activate && python redis_receiver_final.py
```

#### 4. Erro de dependências Python
```bash
# Reinstalar dependências
cd src/main/python
source venv/bin/activate
pip install -r requirements.txt
```

## Desenvolvimento

### Estrutura de Desenvolvimento

1. **Desenvolvimento Java**: Use IntelliJ IDEA ou Eclipse
2. **Desenvolvimento Python**: Use VS Code ou PyCharm
3. **Banco de Dados**: Use pgAdmin para PostgreSQL e MongoDB Compass para MongoDB

### Fluxo de Desenvolvimento

1. **Implementar funcionalidade no Java**
2. **Testar publicação de eventos**
3. **Implementar processamento no Python**
4. **Testar sincronização completa**
5. **Executar testes automatizados**

### Boas Práticas

- **Commits frequentes** com mensagens descritivas
- **Testes unitários** para todas as funcionalidades
- **Documentação** atualizada
- **Logs estruturados** para debugging
- **Validação de dados** em ambas as aplicações

## Documentação Técnica

### Diagramas de Arquitetura
- **Diagrama de Classes**: `docs/diagrama-de-classe-v1.png`
- **Diagrama de Componentes**: `docs/diagrama-componentes.png`
- **Diagrama de Sequência**: `docs/diagrama-sequencia.png`
- **Diagrama de Classes por BD**: `docs/diagrama-classes-bd.png`

### Documentação Específica
- **Sistema Redis**: `src/main/python/README_SISTEMA_COMPLETO.md`
- **API Python**: `src/main/python/README.md`
- **Aplicação Java**: `orm/README.md`

## Contribuição

### Padrões de Código
- **Java**: Seguir convenções Java e usar JavaDoc
- **Python**: Seguir PEP 8 e usar type hints
- **Testes**: Cobertura mínima de 80%
- **Documentação**: Manter README atualizado

### Processo de Desenvolvimento
1. Criar branch para nova funcionalidade
2. Implementar com testes
3. Executar testes completos
4. Criar pull request
5. Code review
6. Merge após aprovação

## Licença

Este projeto é desenvolvido para fins acadêmicos no contexto da disciplina de Software para Persistência de Dados.

## Contato

**Grupo 4 - SPD 2025.3**
- João Pedro Brito
- Leonardo Côrtes  
- Gabriel Mota

---

**Sistema funcionando com sucesso: Java → PostgreSQL → Redis → Python → MongoDB**
