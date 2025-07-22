# repositories/pagamento_repository.py

from models.pagamento import Pagamento

async def criar_pagamento(pagamento: Pagamento) -> Pagamento:
    await pagamento.insert()
    return pagamento

async def buscar_pagamento(id: str) -> Pagamento | None:
    return await Pagamento.get(id)

async def listar_pagamentos() -> list[Pagamento]:
    return await Pagamento.find_all().to_list()
