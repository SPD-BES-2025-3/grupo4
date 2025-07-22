# services/pagamento_service.py

from models.pagamento import Pagamento
from repositories.pagamento_repository import buscar_pagamento

async def processar_pagamento(id: str) -> bool:
    pagamento = await buscar_pagamento(id)
    if pagamento and pagamento.processar():
        await pagamento.save()
        return True
    return False
