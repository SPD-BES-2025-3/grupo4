import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import asyncio
import pytest_asyncio
from faker import Faker
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from models.produto import Produto
from models.item_carrinho import ItemCarrinho  # supondo que esteja neste arquivo

from repositories.repositorio_produto import RepositorioProduto

fake = Faker("pt_BR")
MONGO_TEST_URI = "mongodb://localhost:27017/test_db_item_carrinho"

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
    await init_beanie(database=db, document_models=[Produto])
    yield
    await client.drop_database(db.name)
    client.close()

@pytest_asyncio.fixture
async def repo_produto(init_db, redis_cache):
    return RepositorioProduto(cache=redis_cache)

@pytest_asyncio.fixture
def produto_data():
    return {
        "nome": fake.word().capitalize(),
        "descricao": fake.sentence(),
        "preco": round(fake.pyfloat(left_digits=2, right_digits=2, positive=True), 2),
        "estoque": fake.random_int(min=1, max=100),
        "categoria": fake.word().capitalize(),
    }

@pytest.mark.asyncio
async def test_criar_item_carrinho_e_subtotal(repo_produto, produto_data):
    produto = Produto(**produto_data)
    produto_criado = await repo_produto.criar(produto)

    item = ItemCarrinho(produto=produto_criado, quantidade=4)
    esperado = produto_criado.preco * item.quantidade

    assert item.subtotal() == esperado

def test_str_item_carrinho(repo_produto, produto_data):
    produto = Produto(**produto_data)
    item = ItemCarrinho(produto=produto, quantidade=2)
    texto = str(item)

    assert produto.nome in texto
    assert "R$" in texto
    assert str(item.quantidade) in texto

