from models.produto import Produto
from repositories.repositorio_produto import RepositorioProduto
from api.router_base import criar_crud_router


repositorio = RepositorioProduto()
router = criar_crud_router(Produto, repositorio, "Produto")
