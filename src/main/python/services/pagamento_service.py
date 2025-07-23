# services/pagamento_service.py

from models.pagamento import Pagamento
from main.python.repositories.repositorio_pagamento import RepositorioPagamento

async def processar_pagamento(id: str) -> bool:
    repositorio_pagamento = RepositorioPagamento()
    pagamento = await repositorio_pagamento.buscar_por_id(id)
    if pagamento and pagamento.processar():
        await pagamento.save()
        return True
    return False
