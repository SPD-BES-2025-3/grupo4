from repositories import RepositorioBase, RedisCache
from models.item_carrinho import ItemCarrinho

class RepositorioItemCarrinho(RepositorioBase[ItemCarrinho]):
    """Repositório para operações com ItemCarrinho."""
    def __init__(self, cache: RedisCache | None = None):
        super().__init__(ItemCarrinho, cache)