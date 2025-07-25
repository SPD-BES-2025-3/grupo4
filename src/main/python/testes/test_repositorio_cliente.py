import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import pytest_asyncio
from faker import Faker
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from models.cliente import Cliente
from models.produto import Produto
from models.carrinho import Carrinho
from models.pedido import Pedido

fake = Faker("pt_BR")
MONGO_TEST_URI = "mongodb://localhost:27017/test_db_cliente"

import redis.asyncio as redis
from config.redis_cache import RedisCache

@pytest_asyncio.fixture(scope="function")
async def redis_cache():
    try:
        client = redis.Redis(host="localhost", port=6379, db=1, decode_responses=True)
        await client.ping()
        cache = RedisCache(host="localhost", port=6379, db=1)
        yield cache
        await client.flushdb()
    except redis.ConnectionError:
        pytest.skip("Redis server not available, skipping cache-related tests.")

@pytest_asyncio.fixture(scope="function")
async def init_db():
    client = AsyncIOMotorClient(MONGO_TEST_URI)
    db = client.get_default_database()
    await init_beanie(database=db, document_models=[Cliente, Produto, Carrinho, Pedido])
    yield
    await client.drop_database(db.name)
    client.close()

@pytest_asyncio.fixture
def cliente_data():
    return {
        "nome": fake.name(),
        "email": fake.email(),
        "senha": fake.password(),
        "endereco": fake.address(),
    }

@pytest.mark.asyncio
async def test_criar_cliente(init_db, cliente_data):
    cliente = Cliente(**cliente_data)
    await cliente.insert()

    assert cliente.id is not None
    assert cliente.logado is False

@pytest.mark.asyncio
async def test_buscar_e_atualizar_cliente(init_db, cliente_data):
    cliente = Cliente(**cliente_data)
    await cliente.insert()

    encontrado = await Cliente.get(cliente.id)
    assert encontrado is not None
    assert encontrado.email == cliente_data["email"]

    novo_nome = "Novo Nome"
    encontrado.atualizar_perfil(nome=novo_nome)
    await encontrado.save()

    atualizado = await Cliente.get(cliente.id)
    assert atualizado.nome == novo_nome

@pytest.mark.asyncio
async def test_login_logout_cliente(init_db, cliente_data):
    cliente = Cliente(**cliente_data)
    await cliente.insert()

    assert not cliente.logado
    cliente.login()
    await cliente.save()

    cliente = await Cliente.get(cliente.id)
    assert cliente.logado

    cliente.logout()
    await cliente.save()

    cliente = await Cliente.get(cliente.id)
    assert not cliente.logado

@pytest.mark.asyncio
async def test_deletar_cliente(init_db, cliente_data):
    cliente = Cliente(**cliente_data)
    await cliente.insert()

    id_cliente = cliente.id
    await cliente.delete()

    deletado = await Cliente.get(id_cliente)
    assert deletado is None

@pytest_asyncio.fixture
def produto_data():
    return {
        "nome": fake.word().capitalize(),
        "descricao": fake.sentence(),
        "preco": round(fake.pyfloat(left_digits=2, right_digits=2, positive=True), 2),
        "estoque": fake.random_int(min=10, max=100),
        "categoria": fake.word().capitalize(),
    }

@pytest.mark.asyncio
async def test_adicionar_ao_carrinho(init_db, cliente_data, produto_data):
    cliente = Cliente(**cliente_data)
    produto = Produto(**produto_data)

    await cliente.insert()
    await produto.insert()

    carrinho = await cliente.adicionar_ao_carrinho(produto)
    
    assert carrinho is not None
    assert carrinho.cliente_id == str(cliente.id)
    assert len(carrinho.itens) == 1
    assert carrinho.itens[0].produto.id == produto.id
    assert carrinho.total == produto.preco

@pytest.mark.asyncio
async def test_fazer_pedido(init_db, cliente_data, produto_data):
    cliente = Cliente(**cliente_data)
    produto = Produto(**produto_data)

    await cliente.insert()
    await produto.insert()

    carrinho = await cliente.adicionar_ao_carrinho(produto)
    pedido = await cliente.fazer_pedido()

    assert pedido is not None
    assert str(pedido.cliente.id) == str(cliente.id)
    assert len(pedido.itens) == len(carrinho.itens)
    assert pedido.total == carrinho.total

    carrinho_atualizado = await Carrinho.find_one({"cliente_id": str(cliente.id)})
    assert carrinho_atualizado.total == 0.0
    assert len(carrinho_atualizado.itens) == 0