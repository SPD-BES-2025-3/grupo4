from repositories import RepositorioBase, RedisCache
from models.carrinho import Carrinho

class RepositorioCarrinho(RepositorioBase[Carrinho]):
    """Repositório para operações com Carrinho."""
    def __init__(self, cache: RedisCache | None = None):
        super().__init__(Carrinho, cache)
