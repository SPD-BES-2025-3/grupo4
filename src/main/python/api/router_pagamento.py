from models.pagamento import Pagamento
from repositories.repositorio_pagamento import RepositorioPagamento
from api.router_base import criar_crud_router

repositorio = RepositorioPagamento()
router = criar_crud_router(Pagamento, repositorio, "Pagamento")
