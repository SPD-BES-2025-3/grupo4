from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Olá, mundo com FastAPI!"}

@app.get("/allPayments")
async def all_payments():
    from services.pagamento_service import listar_todos_pagamentos
    pagamentos = await listar_todos_pagamentos()
    return {"pagamentos": pagamentos}