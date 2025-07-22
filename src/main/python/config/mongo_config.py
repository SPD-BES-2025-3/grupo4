# python-backend/src/config/mongo_config.py

import motor.motor_asyncio
from beanie import init_beanie
from pymongo import MongoClient
import asyncio

DATABASE_URL = "mongodb://localhost:27017"
DATABASE_NAME = "ecommerce"

from models.pagamento import Pagamento

client = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URL)
database = client[DATABASE_NAME]

async def init():
    # Initialize Beanie ODM with your database models
    await init_beanie(
        database, 
        document_models=[Pagamento]
    )
