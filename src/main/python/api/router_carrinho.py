from fastapi import HTTPException
from models.carrinho import Carrinho
from models.produto import Produto
from repositories.repositorio_carrinho import RepositorioCarrinho
from api.router_base import criar_crud_router

repositorio = RepositorioCarrinho()
router = criar_crud_router(Carrinho, repositorio, "Carrinho")

# CRUD
## Create
@router.post("/{carrinho_id}/itens", summary="Adicionar item ao carrinho", description="Adiciona um produto ao carrinho especificado pelo ID. É necessário informar o ID do produto e a quantidade desejada. Retorna o carrinho atualizado.")
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
@router.get("/{carrinho_id}/itens/{produto_id}", summary="Obter item do carrinho", description="Retorna os detalhes de um item específico (produto) dentro do carrinho, incluindo nome, quantidade, preço unitário e subtotal. Retorna erro 404 se não encontrado.")
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

@router.get("/{carrinho_id}/itens", summary="Listar itens do carrinho", description="Lista todos os itens presentes no carrinho especificado pelo ID. Retorna uma lista de itens com detalhes de cada produto.")
async def listar_itens(carrinho_id: str):
    carrinho = await Carrinho.get(carrinho_id)
    if not carrinho:
        raise HTTPException(status_code=404, detail="Carrinho não encontrado")
    
    return {"itens": carrinho.itens}

## Update
@router.patch("/{carrinho_id}/itens/{produto_id}", summary="Atualizar quantidade de item no carrinho", description="Atualiza a quantidade de um item (produto) já presente no carrinho. É necessário informar a nova quantidade. Retorna o carrinho atualizado.")
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
@router.delete("/{carrinho_id}/itens/{produto_id}", summary="Remover item do carrinho", description="Remove um item (produto) do carrinho especificado. Retorna mensagem de sucesso ou erro se o item não for encontrado.")
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
