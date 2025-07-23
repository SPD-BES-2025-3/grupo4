from repositories.repositorio_base import RepositorioBase
from models.carrinho import Carrinho

class RepositorioCarrinho(RepositorioBase[Carrinho]):
    """Repositório para operações com Carrinho."""
    def __init__(self):
        super().__init__(Carrinho)
