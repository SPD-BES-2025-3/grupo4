import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import asyncio
import pytest_asyncio
from faker import Faker
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from models.produto import Produto
from models.item_carrinho import ItemCarrinho
from models.carrinho import Carrinho
from repositories.repositorio_produto import RepositorioProduto

fake = Faker("pt_BR")
MONGO_TEST_URI = "mongodb://localhost:27017/test_db_carrinho"

@pytest_asyncio.fixture(scope="function")
async def init_db():
    client = AsyncIOMotorClient(MONGO_TEST_URI)
    db = client.get_default_database()
    await init_beanie(database=db, document_models=[Produto, Carrinho])
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
async def test_adicionar_item_ao_carrinho(repo_produto, produto_data):
    produto = Produto(**produto_data)
    produto_criado = await repo_produto.criar(produto)

    carrinho = Carrinho()
    carrinho.adicionar_item(produto_criado, qtd=2)

    assert len(carrinho.itens) == 1
    assert carrinho.total == produto_criado.preco * 2

@pytest.mark.asyncio
async def test_adicionar_mesmo_produto_incrementa_quantidade(repo_produto, produto_data):
    produto = Produto(**produto_data)
    produto_criado = await repo_produto.criar(produto)

    carrinho = Carrinho()
    carrinho.adicionar_item(produto_criado, qtd=1)
    carrinho.adicionar_item(produto_criado, qtd=3)

    assert len(carrinho.itens) == 1
    assert carrinho.itens[0].quantidade == 4
    assert carrinho.total == produto_criado.preco * 4

@pytest.mark.asyncio
async def test_remover_item_do_carrinho(repo_produto, produto_data):
    produto = Produto(**produto_data)
    produto_criado = await repo_produto.criar(produto)

    carrinho = Carrinho()
    carrinho.adicionar_item(produto_criado, qtd=5)
    carrinho.remover_item(produto_criado)

    assert len(carrinho.itens) == 0
    assert carrinho.total == 0.0

@pytest.mark.asyncio
async def test_esvaziar_carrinho(repo_produto, produto_data):
    produto1 = Produto(**produto_data)
    produto2 = Produto(**produto_data)
    await repo_produto.criar(produto1)
    await repo_produto.criar(produto2)

    carrinho = Carrinho()
    carrinho.adicionar_item(produto1, qtd=1)
    carrinho.adicionar_item(produto2, qtd=2)

    carrinho.esvaziar()

    assert len(carrinho.itens) == 0
    assert carrinho.total == 0.0

@pytest.mark.asyncio
async def test_calcular_total_independente(repo_produto, produto_data):
    produto = Produto(**produto_data)
    produto_criado = await repo_produto.criar(produto)

    carrinho = Carrinho()
    item = ItemCarrinho(produto=produto_criado, quantidade=3)
    carrinho.itens.append(item)

    total = carrinho.calcular_total()
    assert total == produto_criado.preco * 3
