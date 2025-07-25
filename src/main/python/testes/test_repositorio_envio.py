import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import asyncio
import pytest_asyncio
from datetime import datetime
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from faker import Faker
from models.envio import Envio
from repositories.repositorio_base import RepositorioBase

fake = Faker("pt_BR")
MONGO_TEST_URI = "mongodb://localhost:27017/test_db_envio"


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
    await init_beanie(database=db, document_models=[Envio])
    yield
    await client.drop_database(db.name)
    client.close()

@pytest_asyncio.fixture
async def repo(init_db, redis_cache):
    return RepositorioBase(Envio, cache=redis_cache)

@pytest_asyncio.fixture
def envio_data():
    return {
        "endereco_entrega": fake.address(),
        "data_envio": datetime.now(),
        "status": "enviado"
    }

@pytest.mark.asyncio
async def test_criar_e_buscar_por_id(repo, envio_data):
    envio = Envio(**envio_data)
    criado = await repo.criar(envio)
    assert criado.id is not None

    buscado = await repo.buscar_por_id(str(criado.id))
    assert buscado is not None
    assert buscado.id == criado.id

@pytest.mark.asyncio
async def test_listar_todos(repo, envio_data):
    await repo.criar(Envio(**envio_data))
    resultados = await repo.listar_todos()
    assert isinstance(resultados, list)
    assert len(resultados) >= 1

@pytest.mark.asyncio
async def test_atualizar_por_id(repo, envio_data):
    envio = await repo.criar(Envio(**envio_data))
    novo_status = "entregue"
    atualizado = await repo.atualizar_por_id(str(envio.id), {"status": novo_status})
    assert atualizado.status == novo_status

@pytest.mark.asyncio
async def test_atualizar_completo(repo, envio_data):
    envio = await repo.criar(Envio(**envio_data))
    envio.status = "cancelado"
    atualizado = await repo.atualizar_completo(envio)
    assert atualizado.status == "cancelado"

@pytest.mark.asyncio
async def test_deletar_por_id(repo, envio_data):
    envio = await repo.criar(Envio(**envio_data))
    resultado = await repo.deletar_por_id(str(envio.id))
    assert resultado is True

    buscado = await repo.buscar_por_id(str(envio.id))
    assert buscado is None

@pytest.mark.asyncio
async def test_deletar_por_objeto(repo, envio_data):
    envio = await repo.criar(Envio(**envio_data))
    resultado = await repo.deletar_por_objeto(envio)
    assert resultado is True

@pytest.mark.asyncio
async def test_contar_total(repo, envio_data):
    await repo.criar(Envio(**envio_data))
    await repo.criar(Envio(**envio_data))
    total = await repo.contar_total()
    assert total >= 2

@pytest.mark.asyncio
async def test_verificar_existe(repo, envio_data):
    envio = await repo.criar(Envio(**envio_data))
    existe = await repo.verificar_existe(str(envio.id))
    assert existe is True

    nao_existe = await repo.verificar_existe("000000000000000000000000")
    assert nao_existe is False

@pytest.mark.asyncio
async def test_eh_object_id_valido(repo):
    assert repo.eh_object_id_valido("507f1f77bcf86cd799439011")
    assert not repo.eh_object_id_valido("id_invalido")
