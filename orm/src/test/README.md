# Testes Unitários - Aplicação Java

Este diretório contém todos os testes unitários para a aplicação Java, organizados por pacotes e categorias.

## Estrutura dos Testes

### Model (Modelo)
- **UsuarioTest.java** - Testes para a classe Usuario
- **EnderecoTest.java** - Testes para a classe Endereco
- **ClienteCRMTest.java** - Testes para a classe ClienteCRM
- **AdministradorTest.java** - Testes para a classe Administrador
- **ProdutoCRMTest.java** - Testes para a classe ProdutoCRM
- **PedidoCRMTest.java** - Testes para a classe PedidoCRM
- **CarrinhoTest.java** - Testes para a classe Carrinho
- **CarrinhoItemTest.java** - Testes para a classe CarrinhoItem
- **SessaoTest.java** - Testes para a classe Sessao
- **DatabaseTest.java** - Testes para a classe Database
- **RepositorioTest.java** - Testes para a classe Repositorio
- **RepositoriosTest.java** - Testes para a classe Repositorios

### Controller (Controlador)
- **LoginControllerTest.java** - Testes para a classe LoginController
- **CarrinhoControllerTest.java** - Testes para a classe CarrinhoController
- **AbstractCrudControllerTest.java** - Testes para a classe AbstractCrudController

### Redis
- **RedisPublisherTest.java** - Testes para a classe RedisPublisher
- **ProdutoEventPublisherTest.java** - Testes para a classe ProdutoEventPublisher

### View (Visualização)
- **LoginAppViewTest.java** - Testes para a classe LoginAppView

### Main (Principal)
- **MainTest.java** - Testes para a classe Main

### App (Aplicação)
- **AppTest.java** - Testes para a classe App

## Como Executar os Testes

### Usando Maven
```bash
# Executar todos os testes
mvn test

# Executar testes de um pacote específico
mvn test -Dtest=com.exemplo.hello.model.*

# Executar um teste específico
mvn test -Dtest=UsuarioTest
```

### Usando IDE
1. Abra o projeto no seu IDE
2. Navegue até a pasta `src/test/java`
3. Execute os testes individualmente ou em conjunto

## Cobertura de Testes

### Classes Testadas
- ✅ Usuario
- ✅ Endereco
- ✅ ClienteCRM
- ✅ Administrador
- ✅ ProdutoCRM
- ✅ PedidoCRM
- ✅ Carrinho
- ✅ CarrinhoItem
- ✅ Sessao
- ✅ Database
- ✅ Repositorio
- ✅ Repositorios
- ✅ LoginController
- ✅ CarrinhoController
- ✅ AbstractCrudController
- ✅ RedisPublisher
- ✅ ProdutoEventPublisher
- ✅ LoginAppView
- ✅ Main
- ✅ App

### Tipos de Testes Implementados

#### Testes de Modelo
- **Getters e Setters**: Verificação de todos os métodos get/set
- **Construtores**: Teste de criação de objetos
- **Lógica de Negócio**: Teste de métodos específicos da classe
- **Validações**: Teste de casos extremos e inválidos
- **Relacionamentos**: Teste de associações entre objetos

#### Testes de Controller
- **Inicialização**: Teste de criação e setup
- **Métodos de Ação**: Teste de métodos de interface
- **Validações**: Teste de entrada de dados
- **Integração**: Teste de comunicação com modelo

#### Testes de Redis
- **Singleton**: Teste de padrão singleton
- **Publicação**: Teste de publicação de eventos
- **Conexão**: Teste de conexão com Redis
- **Tratamento de Erro**: Teste de exceções

#### Testes de View
- **JavaFX**: Teste de componentes de interface
- **Navegação**: Teste de mudança de telas
- **Inicialização**: Teste de setup da interface

## Dependências de Teste

### JUnit 4
- Framework principal de testes
- Anotações: @Test, @Before, @After
- Assertions: assertEquals, assertNotNull, etc.

### Mockito
- Framework para criação de mocks
- Útil para testar dependências externas
- Anotações: @Mock, @InjectMocks

### TestFX
- Framework para testes de JavaFX
- Teste de componentes de interface
- Anotações: @TestFX

## Padrões de Teste

### Nomenclatura
- Nome da classe: `NomeDaClasseTest`
- Nome dos métodos: `testMetodoQueEstaSendoTestado`
- Exemplo: `testSetAndGetNome()`

### Estrutura
```java
@Test
public void testNomeDoTeste() {
    // Arrange (Preparar)
    // Act (Executar)
    // Assert (Verificar)
}
```

### Casos de Teste
- **Cenário Normal**: Teste do comportamento esperado
- **Cenário Extremo**: Teste com valores limites
- **Cenário de Erro**: Teste de exceções e erros
- **Cenário Nulo**: Teste com valores nulos

## Observações Importantes

### Testes de Integração
Alguns testes dependem de serviços externos (banco de dados, Redis) e podem falhar se esses serviços não estiverem disponíveis. Esses testes são marcados com tratamento de exceção.

### Testes de JavaFX
Testes que envolvem componentes JavaFX podem requerer inicialização especial do toolkit JavaFX.

### Testes de Banco de Dados
Testes que envolvem banco de dados são marcados como testes de integração e podem requerer configuração específica do ambiente.

## Melhorias Futuras

1. **Aumentar Cobertura**: Adicionar mais casos de teste
2. **Testes de Integração**: Criar testes end-to-end
3. **Testes de Performance**: Adicionar testes de carga
4. **Mocks Avançados**: Usar mais mocks para isolar testes
5. **Testes de UI**: Expandir testes de interface gráfica 