from repositories import RepositorioBase, RedisCache
from models.envio import Envio

class RepositorioEnvio(RepositorioBase[Envio]):
    """Repositório para operações com Envio."""
    def __init__(self, cache: RedisCache | None = None):
        super().__init__(Envio, cache)