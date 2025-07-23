import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import asyncio
import pytest_asyncio
from faker import Faker
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from models.produto import Produto
from models.item_pedido import ItemPedido
from repositories.repositorio_produto import RepositorioProduto

fake = Faker("pt_BR")
MONGO_TEST_URI = "mongodb://localhost:27017/test_db_item_pedido"

@pytest_asyncio.fixture(scope="function")
async def init_db():
    client = AsyncIOMotorClient(MONGO_TEST_URI)
    db = client.get_default_database()
    await init_beanie(database=db, document_models=[Produto])
    yield
    await client.drop_database(db.name)
    client.close()

@pytest_asyncio.fixture
async def repo_produto(init_db):
    return RepositorioProduto()

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
async def test_criar_item_pedido_e_subtotal(repo_produto, produto_data):
    # Cria e persiste o produto
    produto = Produto(**produto_data)
    produto_criado = await repo_produto.criar(produto)

    # Cria ItemPedido baseado no Produto
    quantidade = 3
    preco_unitario = produto_criado.preco
    item = ItemPedido(produto=produto_criado, quantidade=quantidade, preco_unitario=preco_unitario)

    # Verifica subtotal
    esperado = quantidade * preco_unitario
    assert item.subtotal() == esperado

@pytest.mark.asyncio
async def test_str_item_pedido(repo_produto, produto_data):
    produto = Produto(**produto_data)
    produto_criado = await repo_produto.criar(produto)

    item = ItemPedido(produto=produto_criado, quantidade=2, preco_unitario=produto_criado.preco)
    string = str(item)

    assert produto_criado.nome in string
    assert "R$" in string
    assert str(item.quantidade) in string
