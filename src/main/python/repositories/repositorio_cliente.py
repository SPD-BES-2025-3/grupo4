from repositories import RepositorioBase, RedisCache
from models.cliente import Cliente

class RepositorioCliente(RepositorioBase[Cliente]):
    """Repositório para operações com Cliente."""
    def __init__(self, cache: RedisCache | None = None):
        super().__init__(Cliente, cache)
