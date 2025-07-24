from models.pedido import Pedido
from repositories.repositorio_pedido import RepositorioPedido
from api.router_base import criar_crud_router

repositorio = RepositorioPedido()
router = criar_crud_router(Pedido, repositorio, "Pedido")
