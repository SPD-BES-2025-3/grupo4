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

    @router.post("/", response_model=modelo_cls)  # You may use `Any` here if Pylance complains
    async def criar(entidade: T):
        return await repositorio.criar(entidade)

    @router.get("/", response_model=List[modelo_cls])
    async def listar_todos():
        return await repositorio.listar_todos()

    @router.get("/{id}", response_model=modelo_cls)
    async def obter_por_id(id: str):
        entidade = await repositorio.buscar_por_id(id)
        if not entidade:
            raise HTTPException(status_code=404, detail=f"{nome} não encontrado")
        return entidade

    @router.put("/{id}", response_model=modelo_cls)
    async def atualizar(id: str, dados: Dict[str, Any]):
        entidade = await repositorio.atualizar_por_id(id, dados)
        if not entidade:
            raise HTTPException(status_code=404, detail=f"{nome} não encontrado")
        return entidade

    @router.delete("/{id}")
    async def deletar(id: str):
        sucesso = await repositorio.deletar_por_id(id)
        if not sucesso:
            raise HTTPException(status_code=404, detail=f"{nome} não encontrado")
        return {"mensagem": f"{nome} deletado com sucesso"}

    return router
