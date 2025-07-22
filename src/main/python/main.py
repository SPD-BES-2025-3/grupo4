# main.py

import asyncio
from config.mongo_config import init
from models.pagamento import Pagamento, DadosPagamento

async def run():
    await init()

    pagamento = Pagamento(
        dados_pagamento=DadosPagamento(tipo="cartao", numero="12345678", validade="12/26"),
        valor=100.50,
        metodo="pix",
        status="pendente"
    )

    await pagamento.insert()
    print(f"Pagamento criado com ID: {pagamento.id}")

if __name__ == "__main__":
    asyncio.run(run())
