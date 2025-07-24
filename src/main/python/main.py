from fastapi import FastAPI
from contextlib import asynccontextmanager
from db.init import init_db  # your DB setup function

from api.router_carrinho import router as carrinho_router
from api.router_cliente import router as cliente_router
from api.router_envio import router as envio_router
from api.router_pagamento import router as pagamento_router
from api.router_pedido import router as pedido_router
from api.router_produto import router as produto_router

app = FastAPI(title="Estoque API")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    await init_db()
    yield
    # Shutdown logic (if needed)
    print("App is shutting down...")

app = FastAPI(lifespan=lifespan)

app.include_router(carrinho_router, prefix="/carrinho", tags=["Carrinho"])
app.include_router(cliente_router, prefix="/cliente", tags=["Cliente"])
app.include_router(envio_router, prefix="/envio", tags=["Envio"])
app.include_router(pagamento_router, prefix="/pagamento", tags=["Pagamento"])
app.include_router(pedido_router, prefix="/pedido", tags=["Pedido"])
app.include_router(produto_router, prefix="/produtos", tags=["Produtos"])
