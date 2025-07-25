from repositories import RepositorioBase, RedisCache
from models.item_pedido import ItemPedido

class RepositorioItemPedido(RepositorioBase[ItemPedido]):
    """Repositório para operações com ItemPedido."""
    def __init__(self, cache: RedisCache | None = None):
        super().__init__(ItemPedido, cache)
