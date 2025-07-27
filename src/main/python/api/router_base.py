from fastapi import APIRouter, HTTPException
from typing import TypeVar, Type, List, Dict, Any
from beanie import Document
from repositories.repositorio_base import RepositorioBase

T = TypeVar("T", bound=Document)

def criar_crud_router(
    modelo_cls: Type[T],
    repositorio: RepositorioBase[T],
    nome: str
) -> APIRouter:
    router = APIRouter()

    @router.post("/", response_model=modelo_cls, summary=f"Criar {nome}", description=f"Cria um novo {nome} no sistema. Recebe um objeto JSON com os dados do {nome} e retorna o objeto criado.")
    async def criar(entidade: T):
        return await repositorio.criar(entidade)

    @router.get("/", response_model=List[modelo_cls], summary=f"Listar todos os {nome}s", description=f"Retorna uma lista com todos os {nome}s cadastrados no sistema.")
    async def listar_todos():
        return await repositorio.listar_todos()

    @router.get("/{id}", response_model=modelo_cls, summary=f"Obter {nome} por ID", description=f"Busca um {nome} pelo seu ID único. Retorna o objeto correspondente ou erro 404 se não encontrado.")
    async def obter_por_id(id: str):
        entidade = await repositorio.buscar_por_id(id)
        if not entidade:
            raise HTTPException(status_code=404, detail=f"{nome} não encontrado")
        return entidade

    @router.put("/{id}", response_model=modelo_cls, summary=f"Atualizar {nome} por ID", description=f"Atualiza um {nome} existente pelo ID. Recebe um dicionário com os campos a serem atualizados e retorna o objeto atualizado.")
    async def atualizar(id: str, dados: Dict[str, Any]):
        entidade = await repositorio.atualizar_por_id(id, dados)
        if not entidade:
            raise HTTPException(status_code=404, detail=f"{nome} não encontrado")
        return entidade

    @router.delete("/{id}", summary=f"Deletar {nome} por ID", description=f"Remove um {nome} do sistema pelo seu ID. Retorna mensagem de sucesso ou erro 404 se não encontrado.")
    async def deletar(id: str):
        sucesso = await repositorio.deletar_por_id(id)
        if not sucesso:
            raise HTTPException(status_code=404, detail=f"{nome} não encontrado")
        return {"mensagem": f"{nome} deletado com sucesso"}

    return router
