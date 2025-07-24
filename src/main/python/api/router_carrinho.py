from models.carrinho import Carrinho
from repositories.repositorio_carrinho import RepositorioCarrinho
from api.router_base import criar_crud_router

repositorio = RepositorioCarrinho()
router = criar_crud_router(Carrinho, repositorio, "Carrinho")
