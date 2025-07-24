from models.cliente import Cliente
from repositories.repositorio_cliente import RepositorioCliente
from api.router_base import criar_crud_router

repositorio = RepositorioCliente()
router = criar_crud_router(Cliente, repositorio, "Cliente")
