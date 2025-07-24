from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from models.carrinho import Carrinho
from models.cliente import Cliente
from models.envio import Envio
from models.pagamento import Pagamento
from models.pedido import Pedido
from models.produto import Produto

import os

async def init_db():
    client = AsyncIOMotorClient("mongodb://localhost:27017")  # Adjust for your URI
    await init_beanie(database=client["ecommerce"], document_models=[Carrinho, Cliente, Envio, Pagamento, Pedido, Produto])
