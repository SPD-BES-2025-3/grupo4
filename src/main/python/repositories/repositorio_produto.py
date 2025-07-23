from repositories.repositorio_base import RepositorioBase
from models.produto import Produto

class RepositorioProduto(RepositorioBase[Produto]):
    """Repositório para operações com Produto."""
    def __init__(self):
        super().__init__(Produto)