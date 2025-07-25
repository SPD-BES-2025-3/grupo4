import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import pytest_asyncio
from datetime import datetime
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from faker import Faker

from models.produto import Produto
from models.cliente import Cliente
from models.pedido import Pedido
from models.item_pedido import ItemPedido
from models.carrinho import Carrinho
from models.item_carrinho import ItemCarrinho

fake = Faker("pt_BR")
MONGO_TEST_URI = "mongodb://localhost:27017/test_db_pedido"

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
    await init_beanie(database=db, document_models=[Produto, Cliente, Pedido, Carrinho])
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
async def test_criar_a_partir_do_carrinho(init_db, cliente_data, produto_data):
    cliente = Cliente(**cliente_data)
    produto = Produto(**produto_data)
    await cliente.insert()
    await produto.insert()

    carrinho = Carrinho(cliente_id=str(cliente.id))
    carrinho.adicionar_item(produto, qtd=2)
    await carrinho.insert()

    pedido = await Pedido.criar_a_partir_do_carrinho(cliente, carrinho)
    assert pedido.total == produto.preco * 2
    assert pedido.status == "pendente"
    assert pedido.cliente.id == cliente.id
    assert len(pedido.itens) == 1
    assert pedido.itens[0].quantidade == 2

@pytest.mark.asyncio
async def test_cancelar_e_atualizar_status(init_db, cliente_data):
    cliente = Cliente(**cliente_data)
    await cliente.insert()

    pedido = Pedido(cliente=cliente, total=100.0)
    await pedido.insert()

    # Atualizar status
    pedido.atualizar_status("confirmado")
    assert pedido.status == "confirmado"

    # Cancelar
    pedido.cancelar()
    assert pedido.status == "cancelado"

    # Status entregado não permite cancelamento
    pedido.status = "entregue"
    pedido.cancelar()
    assert pedido.status == "entregue"

@pytest.mark.asyncio
async def test_str_pedido(init_db, cliente_data):
    cliente = Cliente(**cliente_data)
    await cliente.insert()

    pedido = Pedido(cliente=cliente, total=42.5)
    await pedido.insert()

    texto = str(pedido)
    assert f"Pedido de R$ {pedido.total:.2f}" in texto
    assert pedido.status in texto
    assert pedido.data_pedido.strftime('%d/%m/%Y') in texto
