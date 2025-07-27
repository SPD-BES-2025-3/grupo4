from typing import Literal, Optional
from models.pedido import Pedido
from repositories.repositorio_pedido import RepositorioPedido
from api.router_base import criar_crud_router
from fastapi import HTTPException

repositorio = RepositorioPedido()
router = criar_crud_router(Pedido, repositorio, "Pedido")

@router.patch("/{pedido_id}/status", summary="Atualizar status do pedido", description="Atualiza o status de um pedido existente. O novo status deve ser um dos seguintes: pendente, confirmado, enviado, entregue ou cancelado. Retorna o pedido atualizado.")
async def atualizar_status(pedido_id: str, novo_status: Literal["pendente", "confirmado", "enviado", "entregue", "cancelado"]):
    pedido = await Pedido.get(pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    pedido.atualizar_status(novo_status)
    await pedido.save()
    return pedido

@router.get("/{pedido_id}/resumo", summary="Resumo do pedido", description="Retorna um resumo do pedido, incluindo o valor total, lista de itens e status atual. Útil para exibir informações consolidadas ao usuário.")
async def resumo_do_pedido(pedido_id: str):
    pedido = await Pedido.get(pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    return {
        "total": pedido.total,
        "itens": [str(item) for item in pedido.itens],
        "status": pedido.status
    }

# CRUD
## Create
@router.post("/cliente/{cliente_id}/carrinho/{carrinho_id}", response_model=Pedido, summary="Criar pedido a partir do carrinho", description="Cria um novo pedido para um cliente a partir de um carrinho existente. É necessário informar os IDs do cliente e do carrinho. Retorna o pedido criado.")
async def criar_pedido_do_carrinho(cliente_id: str, carrinho_id: str):
    from models.cliente import Cliente
    from models.carrinho import Carrinho

    cliente = await Cliente.get(cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    carrinho = await Carrinho.get(carrinho_id)
    if not carrinho:
        raise HTTPException(status_code=404, detail="Carrinho não encontrado")

    pedido = await Pedido.criar_a_partir_do_carrinho(cliente, carrinho)
    await pedido.insert()
    return pedido

## Retrieve
@router.get("/{pedido_id}/itens/{produto_id}", summary="Obter item do pedido", description="Retorna os detalhes de um item específico dentro do pedido, incluindo nome do produto, quantidade, preço unitário e subtotal. Retorna erro 404 se não encontrado.")
async def obter_item_pedido(pedido_id: str, produto_id: str):
    pedido = await Pedido.get(pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    for item in pedido.itens:
        if item.produto.id == produto_id:
            return {
                "produto": item.produto.nome,
                "quantidade": item.quantidade,
                "preco_unitario": item.preco_unitario,
                "subtotal": item.subtotal()
            }

    raise HTTPException(status_code=404, detail="Item não encontrado no pedido")

@router.get("/{pedido_id}/itens", summary="Listar itens do pedido", description="Lista todos os itens presentes no pedido especificado pelo ID. Retorna uma lista de itens com detalhes de cada produto.")
async def listar_itens(pedido_id: str):
    pedido = await Pedido.get(pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    
    return {"itens": pedido.itens}

## Update
@router.patch("/{pedido_id}/itens/{produto_id}", summary="Atualizar item do pedido", description="Atualiza a quantidade e/ou preço unitário de um item já presente no pedido. Retorna o pedido atualizado.")
async def atualizar_item_pedido(
    pedido_id: str,
    produto_id: str,
    nova_quantidade: Optional[int] = None,
    novo_preco_unitario: Optional[float] = None
):
    if pedido.status in ["cancelado", "entregue"]:
        raise HTTPException(status_code=400, detail="Status não pode ser alterado neste estado")

    pedido = await Pedido.get(pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    if nova_quantidade is not None and nova_quantidade <= 0:
        raise HTTPException(status_code=400, detail="Quantidade deve ser maior que zero")
    if novo_preco_unitario is not None and novo_preco_unitario <= 0:
        raise HTTPException(status_code=400, detail="Preço unitário deve ser positivo")

    for item in pedido.itens:
        if item.produto.id == produto_id:
            if nova_quantidade:
                item.quantidade = nova_quantidade
            if novo_preco_unitario:
                item.preco_unitario = novo_preco_unitario

            pedido.total = sum(i.subtotal() for i in pedido.itens)
            await pedido.save()
            return pedido

    raise HTTPException(status_code=404, detail="Item não encontrado no pedido")

## Delete
@router.delete("/{pedido_id}/itens/{produto_id}", summary="Remover item do pedido", description="Remove um item (produto) do pedido especificado. Retorna mensagem de sucesso ou erro se o item não for encontrado ou se o pedido ficar vazio.")
async def remover_item_pedido(pedido_id: str, produto_id: str):
    pedido = await Pedido.get(pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    itens_filtrados = [item for item in pedido.itens if item.produto.id != produto_id]

    if len(itens_filtrados) == len(pedido.itens):
        raise HTTPException(status_code=404, detail="Item não encontrado no pedido")

    pedido.itens = itens_filtrados
    if not pedido.itens:
        raise HTTPException(status_code=400, detail="Pedido não pode ficar vazio")

    pedido.total = sum(item.subtotal() for item in pedido.itens)
    await pedido.save()
    return {"mensagem": "Item removido do pedido com sucesso"}
