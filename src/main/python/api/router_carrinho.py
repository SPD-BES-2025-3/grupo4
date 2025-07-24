from fastapi import HTTPException
from models.carrinho import Carrinho
from models.produto import Produto
from repositories.repositorio_carrinho import RepositorioCarrinho
from api.router_base import criar_crud_router

repositorio = RepositorioCarrinho()
router = criar_crud_router(Carrinho, repositorio, "Carrinho")

# CRUD
## Create
@router.post("/{carrinho_id}/itens")
async def adicionar_item(carrinho_id: str, produto_id: str, quantidade: int):
    carrinho = await Carrinho.get(carrinho_id)
    if not carrinho:
        raise HTTPException(status_code=404, detail="Carrinho não encontrado")
    if quantidade <= 0:
        raise HTTPException(status_code=400, detail="Quantidade deve ser positiva")

    produto = await Produto.get(produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    carrinho.adicionar_item(produto, quantidade)
    await carrinho.save()
    return carrinho

## Retrieve
@router.get("/{carrinho_id}/itens/{produto_id}")
async def obter_item_carrinho(carrinho_id: str, produto_id: str):
    carrinho = await Carrinho.get(carrinho_id)
    if not carrinho:
        raise HTTPException(status_code=404, detail="Carrinho não encontrado")

    for item in carrinho.itens:
        if item.produto.id == produto_id:
            return {
                "produto": item.produto.nome,
                "quantidade": item.quantidade,
                "preco_unitario": item.produto.preco,
                "subtotal": item.subtotal()
            }

    raise HTTPException(status_code=404, detail="Item não encontrado no carrinho")

@router.get("/{carrinho_id}/itens")
async def listar_itens(carrinho_id: str):
    carrinho = await Carrinho.get(carrinho_id)
    if not carrinho:
        raise HTTPException(status_code=404, detail="Carrinho não encontrado")
    
    return {"itens": carrinho.itens}

## Update
@router.patch("/{carrinho_id}/itens/{produto_id}")
async def atualizar_quantidade_item(carrinho_id: str, produto_id: str, nova_quantidade: int):
    carrinho = await Carrinho.get(carrinho_id)
    if not carrinho:
        raise HTTPException(status_code=404, detail="Carrinho não encontrado")
    if nova_quantidade <= 0:
        raise HTTPException(status_code=400, detail="Quantidade deve ser maior que zero")

    produto = await Produto.get(produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    for item in carrinho.itens:
        if item.produto.id == produto.id:
            item.quantidade = nova_quantidade
            await carrinho.calcular_total()
            await carrinho.save()
            return carrinho

    raise HTTPException(status_code=404, detail="Item não encontrado no carrinho")

## Delete
@router.delete("/{carrinho_id}/itens/{produto_id}")
async def remover_item(carrinho_id: str, produto_id: str):
    carrinho = await Carrinho.get(carrinho_id)
    if not carrinho:
        raise HTTPException(status_code=404, detail="Carrinho não encontrado")

    produto = await Produto.get(produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    carrinho.remover_item(produto)
    await carrinho.calcular_total()
    await carrinho.save()
    return {"mensagem": "Item removido com sucesso"}
