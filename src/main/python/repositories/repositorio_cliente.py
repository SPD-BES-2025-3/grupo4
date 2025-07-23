from repositories.repositorio_base import RepositorioBase
from models.cliente import Cliente

class RepositorioCliente(RepositorioBase[Cliente]):
    """Repositório para operações com Cliente."""
    def __init__(self):
        super().__init__(Cliente)
