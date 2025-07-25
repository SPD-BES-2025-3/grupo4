from repositories import RepositorioBase, RedisCache
from models.pedido import Pedido

class RepositorioPedido(RepositorioBase[Pedido]):
    """Repositório para operações com Pedido."""
    def __init__(self, cache: RedisCache | None = None):
        super().__init__(Pedido, cache)
