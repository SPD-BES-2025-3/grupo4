# Sistema de Sincronização Redis - Produtos

Este sistema permite a sincronização de produtos entre PostgreSQL (Java) e MongoDB (Python) usando Redis como intermediário.

## Arquitetura

```
PostgreSQL (Java) → Redis → MongoDB (Python)
```

### Fluxo de Dados

1. **Java (PostgreSQL)**: Publica eventos de produtos no canal `produtos` do Redis
2. **Redis**: Atua como message broker entre os sistemas
3. **Python (MongoDB)**: Recebe os eventos e sincroniza os dados no MongoDB

## Como Usar

### 1. Pré-requisitos

Certifique-se de que os seguintes serviços estão rodando:

- **Redis**: `localhost:6379`
- **MongoDB**: `localhost:27017`

### 2. Executar o Receptor Redis

```bash
# Navegar para o diretório Python
cd src/main/python

# Executar o receptor Redis
python redis_receiver.py
```

O receptor irá:

- Conectar ao Redis e MongoDB
- Escutar o canal `produtos`
- Processar eventos de produtos (CREATE, UPDATE, DELETE)
- Sincronizar dados no MongoDB

### 3. Testar o Sistema

Em outro terminal, execute o simulador:

```bash
# Executar simulador de envio
python test_redis_sender.py
```

Isso irá enviar produtos de teste para o Redis, simulando dados vindos do Java.

## 📊 Eventos Suportados

### CREATE

```json
{
  "acao": "CREATE",
  "produto": {
    "id": 1,
    "nome": "Notebook Dell Inspiron",
    "descricao": "Notebook Dell Inspiron 15 polegadas",
    "preco": 2999.99,
    "estoque": 10,
    "categoria": "Informática"
  }
}
```

### UPDATE

```json
{
  "acao": "UPDATE",
  "produto": {
    "id": 1,
    "nome": "Notebook Dell Inspiron",
    "descricao": "Notebook Dell Inspiron 15 polegadas, 16GB RAM",
    "preco": 3499.99,
    "estoque": 8,
    "categoria": "Informática"
  }
}
```

### DELETE

```json
{
  "acao": "DELETE",
  "produto": {
    "id": 3,
    "nome": "Mouse USB Logitech",
    "descricao": "Mouse USB Logitech M185",
    "preco": 29.99,
    "estoque": 50,
    "categoria": "Informática"
  }
}
```

## 🔧 Configuração

### Variáveis de Ambiente (Opcional)

```bash
# Redis
export REDIS_HOST=localhost
export REDIS_PORT=6379

# MongoDB
export MONGO_URI=mongodb://localhost:27017
```

### Configuração no Código

Edite as configurações em `redis_receiver.py`:

```python
# Configurações
redis_host = "localhost"
redis_port = 6379
mongo_uri = "mongodb://localhost:27017"
```

## 📝 Logs

O sistema gera logs detalhados:

- **Arquivo**: `redis_receiver.log`
- **Console**: Logs em tempo real
- **Nível**: INFO

### Exemplo de Logs

```
2024-01-01 10:00:00 - Conectado ao Redis com sucesso
2024-01-01 10:00:01 - Conectado ao MongoDB com sucesso
2024-01-01 10:00:02 - Iniciando escuta do canal 'produtos' no Redis...
2024-01-01 10:00:05 - Processando evento de produto: CREATE - Notebook Dell Inspiron
2024-01-01 10:00:05 - Produto criado com sucesso: Notebook Dell Inspiron
```

## Troubleshooting

### Erro de Conexão Redis

```
Erro ao conectar ao Redis: Connection refused
```

**Solução**: Verifique se o Redis está rodando em `localhost:6379`

### Erro de Conexão MongoDB

```
Erro ao conectar ao MongoDB: Connection refused
```

**Solução**: Verifique se o MongoDB está rodando em `localhost:27017`

### Produto não encontrado

```
 Produto não encontrado para atualização: Nome do Produto
```

**Solução**: O produto será criado automaticamente se não existir

## Monitoramento

### Verificar Produtos no MongoDB

```python
from models.produto import Produto
import motor.motor_asyncio

# Conectar ao MongoDB
client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
await Produto.init_beanie(database=client.ecommerce)

# Listar produtos
produtos = await Produto.find_all().to_list()
for produto in produtos:
    print(f"{produto.nome} - R$ {produto.preco:.2f}")
```

### Verificar Canal Redis

```python
from redis import Redis

redis_client = Redis(host="localhost", port=6379)
# Verificar se o canal está ativo
print(redis_client.pubsub_channels())
```

## Integração com Java

Para integrar com o sistema Java existente, certifique-se de que:

1. **ProdutoEventPublisher.java** está publicando no canal `produtos`
2. **Formato JSON** está compatível com o esperado pelo Python
3. **Redis** está acessível para ambos os sistemas

### Exemplo de Integração Java

```java
// No Java, usar ProdutoEventPublisher
ProdutoCRM produto = new ProdutoCRM();
produto.setNome("Novo Produto");
produto.setPreco(99.99);
produto.setEstoque(10);

ProdutoEventPublisher.publicarEvento("CREATE", produto);
```

## Checklist de Verificação

### Antes de Executar

- [ ] Redis rodando em `localhost:6379`
- [ ] MongoDB rodando em `localhost:27017`
- [ ] Dependências Python instaladas (`pip install -r requirements.txt`)

### Durante a Execução

- [ ] Receptor Redis conectado
- [ ] MongoDB conectado
- [ ] Canal `produtos` sendo monitorado
- [ ] Logs aparecendo no console

### Após Testes

- [ ] Produtos sendo criados no MongoDB
- [ ] Produtos sendo atualizados corretamente
- [ ] Produtos sendo deletados quando necessário
- [ ] Logs mostrando sucesso nas operações

## Próximos Passos

1. **Integração Completa**: Conectar com o sistema Java real
2. **Monitoramento**: Adicionar métricas e alertas
3. **Escalabilidade**: Implementar cluster Redis
4. **Segurança**: Adicionar autenticação Redis
5. **Backup**: Implementar backup automático dos dados

## 📞 Suporte

Para dúvidas ou problemas:

1. Verifique os logs em `redis_receiver.log`
2. Teste a conectividade com Redis e MongoDB
3. Execute o simulador para verificar o fluxo
4. Verifique se o formato JSON está correto
