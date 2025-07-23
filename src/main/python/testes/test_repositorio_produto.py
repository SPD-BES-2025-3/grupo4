import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import asyncio
import pytest_asyncio
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from faker import Faker
from models.produto import Produto
from repositories.repositorio_produto import RepositorioProduto

# Configuração de ambiente
fake = Faker("pt_BR")
MONGO_TEST_URI = "mongodb://localhost:27017/test_db_produto"


@pytest_asyncio.fixture(scope="function")
async def init_db():
    client = AsyncIOMotorClient(MONGO_TEST_URI)
    db = client.get_default_database()
    await init_beanie(database=db, document_models=[Produto])
    yield
    await client.drop_database(db.name)
    client.close()

@pytest_asyncio.fixture
async def repo(init_db):
    return RepositorioProduto()

@pytest_asyncio.fixture
def produto_data():
    return {
        "nome": fake.word().capitalize(),
        "descricao": fake.sentence(),
        "preco": round(fake.pyfloat(left_digits=2, right_digits=2, positive=True), 2),
        "estoque": fake.random_int(min=0, max=100),
        "categoria": fake.word().capitalize(),
    }

@pytest.mark.asyncio
async def test_criar_e_buscar_por_id(repo, produto_data):
    produto = Produto(**produto_data)
    criado = await repo.criar(produto)
    assert criado.id is not None

    buscado = await repo.buscar_por_id(str(criado.id))
    assert buscado is not None
    assert buscado.id == criado.id

@pytest.mark.asyncio
async def test_listar_todos(repo, produto_data):
    await repo.criar(Produto(**produto_data))
    resultados = await repo.listar_todos()
    assert isinstance(resultados, list)
    assert len(resultados) >= 1

@pytest.mark.asyncio
async def test_atualizar_por_id(repo, produto_data):
    produto = await repo.criar(Produto(**produto_data))
    atualizado = await repo.atualizar_por_id(str(produto.id), {"descricao": "Descrição atualizada"})
    assert atualizado.descricao == "Descrição atualizada"

@pytest.mark.asyncio
async def test_atualizar_completo(repo, produto_data):
    produto = await repo.criar(Produto(**produto_data))
    produto.nome = "Novo Nome"
    atualizado = await repo.atualizar_completo(produto)
    assert atualizado.nome == "Novo Nome"

@pytest.mark.asyncio
async def test_deletar_por_id(repo, produto_data):
    produto = await repo.criar(Produto(**produto_data))
    resultado = await repo.deletar_por_id(str(produto.id))
    assert resultado is True

    buscado = await repo.buscar_por_id(str(produto.id))
    assert buscado is None

@pytest.mark.asyncio
async def test_deletar_por_objeto(repo, produto_data):
    produto = await repo.criar(Produto(**produto_data))
    resultado = await repo.deletar_por_objeto(produto)
    assert resultado is True

@pytest.mark.asyncio
async def test_contar_total(repo, produto_data):
    await repo.criar(Produto(**produto_data))
    await repo.criar(Produto(**produto_data))
    total = await repo.contar_total()
    assert total >= 2

@pytest.mark.asyncio
async def test_verificar_existe(repo, produto_data):
    produto = await repo.criar(Produto(**produto_data))
    existe = await repo.verificar_existe(str(produto.id))
    assert existe is True

    nao_existe = await repo.verificar_existe("000000000000000000000000")
    assert nao_existe is False

@pytest.mark.asyncio
async def test_eh_object_id_valido(repo):
    assert repo.eh_object_id_valido("507f1f77bcf86cd799439011")
    assert not repo.eh_object_id_valido("id_invalido")
