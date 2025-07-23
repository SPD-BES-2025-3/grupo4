import pytest
from bson import ObjectId

class TestRepositorioBaseCompleto:
    """Testes genéricos para RepositorioBase."""

    @pytest.mark.unit
    async def test_eh_object_id_valido(self, repo):
        assert repo.eh_object_id_valido("507f191e810c19729de860ea") is True
        assert repo.eh_object_id_valido("invalid_id") is False
        assert repo.eh_object_id_valido("") is False
        assert repo.eh_object_id_valido(None) is False

    @pytest.mark.asyncio
    async def test_criar_e_buscar_por_id(self, repo, modelo_data, modelo_cls):
        entidade = modelo_cls(**modelo_data)
        criado = await repo.criar(entidade)
        assert criado.id is not None

        buscado = await repo.buscar_por_id(str(criado.id))
        assert buscado is not None
        assert buscado.id == criado.id

    @pytest.mark.asyncio
    async def test_listar_todos(self, repo, modelo_data, modelo_cls):
        entidade = modelo_cls(**modelo_data)
        await repo.criar(entidade)

        resultados = await repo.listar_todos()
        assert isinstance(resultados, list)
        assert any(r.id == entidade.id for r in resultados)

    @pytest.mark.asyncio
    async def test_atualizar_por_id(self, repo, modelo_data, modelo_cls):
        entidade = modelo_cls(**modelo_data)
        criado = await repo.criar(entidade)

        atualizados = {"status": "atualizado"}  # campo genérico
        atualizado = await repo.atualizar_por_id(str(criado.id), atualizados)

        assert atualizado is not None
        assert atualizado.status == "atualizado"

    @pytest.mark.asyncio
    async def test_atualizar_completo(self, repo, modelo_data, modelo_cls):
        entidade = modelo_cls(**modelo_data)
        criado = await repo.criar(entidade)
        criado.status = "completo"
        atualizado = await repo.atualizar_completo(criado)

        assert atualizado is not None
        assert atualizado.status == "completo"

    @pytest.mark.asyncio
    async def test_deletar_por_id(self, repo, modelo_data, modelo_cls):
        entidade = modelo_cls(**modelo_data)
        criado = await repo.criar(entidade)

        deletado = await repo.deletar_por_id(str(criado.id))
        assert deletado is True

        buscado = await repo.buscar_por_id(str(criado.id))
        assert buscado is None

    @pytest.mark.asyncio
    async def test_deletar_por_objeto(self, repo, modelo_data, modelo_cls):
        entidade = modelo_cls(**modelo_data)
        criado = await repo.criar(entidade)

        deletado = await repo.deletar_por_objeto(criado)
        assert deletado is True

        buscado = await repo.buscar_por_id(str(criado.id))
        assert buscado is None

    @pytest.mark.asyncio
    async def test_contar_total(self, repo, modelo_data, modelo_cls):
        await repo.criar(modelo_cls(**modelo_data))
        await repo.criar(modelo_cls(**modelo_data))

        total = await repo.contar_total()
        assert total >= 2

    @pytest.mark.asyncio
    async def test_verificar_existe(self, repo, modelo_data, modelo_cls):
        entidade = modelo_cls(**modelo_data)
        criado = await repo.criar(entidade)

        existe = await repo.verificar_existe(str(criado.id))
        assert existe is True

        existe_falso = await repo.verificar_existe("507f191e810c19729de860ea")
        assert existe_falso is False
