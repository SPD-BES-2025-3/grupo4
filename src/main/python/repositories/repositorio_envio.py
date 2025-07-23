from repositories.repositorio_base import RepositorioBase
from models.envio import Envio

class RepositorioEnvio(RepositorioBase[Envio]):
    """Repositório para operações com Envio."""
    def __init__(self):
        super().__init__(Envio)