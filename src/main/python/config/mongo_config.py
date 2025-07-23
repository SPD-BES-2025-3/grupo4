# python-backend/src/config/mongo_config.py

import motor.motor_asyncio
from beanie import init_beanie
from pymongo import MongoClient
import asyncio

DATABASE_URL = "mongodb://localhost:27017"
DATABASE_NAME = "ecommerce"

from models.carrinho import Carrinho
from models.cliente import Cliente
from models.envio import Envio
from models.pagamento import Pagamento
from models.pedido import Pedido
from models.produto import Produto

client = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URL)
database = client[DATABASE_NAME]

async def init():
    # Initialize Beanie ODM with your database models
    await init_beanie(
        database, 
        document_models=[Carrinho, Cliente, Envio, Pagamento, Pedido, Produto]
    )
