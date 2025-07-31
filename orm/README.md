# Aplicação Java - CRM E-commerce

## Visão Geral

Esta é a aplicação desktop Java que funciona como CRM (Customer Relationship Management) do sistema de e-commerce. Desenvolvida com JavaFX, utiliza PostgreSQL para persistência de dados e publica eventos via Redis para sincronização com o backend Python.

## Arquitetura

### Tecnologias Utilizadas
- **Java 21** - Linguagem principal
- **JavaFX** - Interface gráfica desktop
- **ORMLite** - ORM para PostgreSQL
- **PostgreSQL** - Banco de dados relacional
- **Maven** - Gerenciamento de dependências
- **JUnit 4** - Testes unitários
- **Mockito** - Framework de mocking
- **Redis (Lettuce)** - Cliente Redis para publicação de eventos

### Estrutura do Projeto
```
orm/
├── src/main/java/com/exemplo/hello/
│   ├── controller/           # Controladores JavaFX
│   │   ├── AbstractCrudController.java
│   │   ├── ProdutosController.java
│   │   ├── ClientesController.java
│   │   ├── CarrinhoController.java
│   │   └── ...
│   ├── model/               # Entidades de domínio
│   │   ├── ProdutoCRM.java
│   │   ├── ClienteCRM.java
│   │   ├── PedidoCRM.java
│   │   ├── Carrinho.java
│   │   └── ...
│   ├── redis/               # Publicadores Redis
│   │   ├── ProdutoEventPublisher.java
│   │   └── RedisPublisher.java
│   ├── view/                # Views JavaFX
│   │   ├── ProdutosView.java
│   │   ├── ClientesView.java
│   │   └── ...
│   ├── main/                # Classes principais
│   │   ├── Main.java
│   │   └── Database.java
│   └── Repositorio.java     # Interface de repositório
├── src/main/resources/
│   └── view/                # Arquivos FXML
│       ├── Produtos.fxml
│       ├── Clientes.fxml
│       └── ...
├── src/test/java/           # Testes unitários
├── pom.xml                  # Dependências Maven
└── docker-compose.yml       # Configuração Docker
```

## Funcionalidades

### Gerenciamento de Produtos
- **CRUD Completo**: Criar, ler, atualizar e deletar produtos
- **Interface Gráfica**: JavaFX com tabelas e formulários
- **Validação de Dados**: Validação em tempo real
- **Publicação de Eventos**: Sincronização automática via Redis

### Gerenciamento de Clientes
- **Cadastro de Clientes**: Informações pessoais e endereço
- **Consulta e Edição**: Interface para gerenciar clientes
- **Validação**: Verificação de dados obrigatórios

### Carrinho de Compras
- **Adicionar Produtos**: Seleção de produtos e quantidades
- **Remover Produtos**: Remoção de itens do carrinho
- **Cálculo de Total**: Soma automática dos valores
- **Validação de Estoque**: Verificação de disponibilidade

### Sistema de Eventos
- **Publicação Redis**: Eventos de produtos (CREATE, UPDATE, DELETE)
- **Formato JSON**: Dados estruturados para sincronização
- **Logs Detalhados**: Monitoramento de operações

## Como Executar

### Pré-requisitos
1. **Java 21** instalado
2. **Maven** instalado
3. **PostgreSQL** rodando
4. **Redis** rodando

### Configuração

#### 1. Configurar Banco de Dados
```bash
# Verificar se PostgreSQL está rodando
psql -U postgres -d projetospd

# Criar tabelas (se necessário)
# As tabelas são criadas automaticamente pelo ORMLite
```

#### 2. Configurar Redis
```bash
# Verificar se Redis está rodando
redis-cli ping

# Se não estiver rodando
redis-server --daemonize yes
```

#### 3. Compilar Projeto
```bash
cd orm
mvn clean install
```

#### 4. Executar Aplicação
```bash
mvn javafx:run
```

### Configurações de Conexão

#### Banco de Dados (Main.java)
```java
private static final String DATABASE_URL = "jdbc:postgresql://localhost:5432/projetospd";
private static final String USER = "postgres";
private static final String PASSWORD = "123456";
```

#### Redis (ProdutoEventPublisher.java)
```java
private static final RedisClient redisClient = RedisClient.create("redis://localhost:6379");
```

## Desenvolvimento

### Estrutura MVC
- **Model**: Entidades em `model/`
- **View**: Interfaces FXML em `resources/view/`
- **Controller**: Controladores em `controller/`

### Padrões Utilizados
- **Repository Pattern**: Interface `Repositorio<T, ID>`
- **Observer Pattern**: Eventos Redis
- **Factory Pattern**: Criação de repositórios
- **Singleton Pattern**: Instâncias únicas

### Testes

#### Executar Testes
```bash
mvn test
```

#### Cobertura de Testes
- **Modelos**: Testes de entidades
- **Controladores**: Testes de lógica de negócio
- **Repositórios**: Testes de persistência
- **Redis**: Testes de publicação de eventos

### Logs e Debug

#### Logs da Aplicação
- **Console**: Logs de operações CRUD
- **Redis**: Logs de publicação de eventos
- **Database**: Logs de conexão e queries

#### Exemplo de Log
```
Salvando produto:
Nome: Produto Teste
Descrição: Descrição do produto
Preço: 99.99
Estoque: 10
Evento publicado no Redis: {"acao":"criado","produto":{"id":0,"nome":"Produto Teste",...}}
```

## Integração com Sistema Python

### Eventos Publicados
- **CREATE**: Quando produto é criado
- **UPDATE**: Quando produto é atualizado
- **DELETE**: Quando produto é removido

### Formato dos Eventos
```json
{
  "acao": "criado",
  "produto": {
    "id": 0,
    "nome": "Nome do Produto",
    "descricao": "Descrição do produto",
    "preco": 99.99,
    "estoque": 10
  }
}
```

### Canais Redis
- **produtos**: Eventos de produtos
- **carrinho:{cliente_id}**: Eventos de carrinho por cliente

## Troubleshooting

### Problemas Comuns

#### 1. Erro de Conexão PostgreSQL
```bash
# Verificar se PostgreSQL está rodando
sudo systemctl status postgresql

# Verificar conexão
psql -U postgres -d projetospd
```

#### 2. Erro de Conexão Redis
```bash
# Verificar se Redis está rodando
redis-cli ping

# Iniciar Redis
redis-server --daemonize yes
```

#### 3. Erro de Compilação Maven
```bash
# Limpar e recompilar
mvn clean install

# Verificar dependências
mvn dependency:tree
```

#### 4. Erro de Interface JavaFX
```bash
# Verificar versão do Java
java -version

# Verificar módulos JavaFX
java --list-modules | grep javafx
```

## Boas Práticas

### Código
- **Nomenclatura**: Seguir convenções Java
- **Documentação**: JavaDoc para métodos públicos
- **Validação**: Validar dados de entrada
- **Tratamento de Erros**: Try-catch apropriados

### Testes
- **Cobertura**: Mínimo 80% de cobertura
- **Testes Unitários**: Para todas as classes
- **Testes de Integração**: Para repositórios
- **Mocks**: Para dependências externas

### Logs
- **Níveis**: INFO, WARNING, ERROR
- **Contexto**: Incluir informações relevantes
- **Performance**: Evitar logs excessivos

## Contribuição

### Padrões de Commit
```
feat: adicionar funcionalidade de produto
fix: corrigir erro de validação
test: adicionar testes para ProdutoCRM
docs: atualizar documentação
```

### Processo de Desenvolvimento
1. Criar branch para funcionalidade
2. Implementar com testes
3. Executar testes completos
4. Criar pull request
5. Code review
6. Merge após aprovação

---

**Aplicação Java funcionando com sucesso e sincronizando com Python via Redis**
