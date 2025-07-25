from repositories import RepositorioBase, RedisCache
from models.produto import Produto

class RepositorioProduto(RepositorioBase[Produto]):
    """Repositório para operações com Produto."""
    def __init__(self, cache: RedisCache | None = None):
        super().__init__(Produto, cache)
