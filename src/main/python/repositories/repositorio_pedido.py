from repositories.repositorio_base import RepositorioBase
from models.pedido import Pedido

class RepositorioPedido(RepositorioBase[Pedido]):
    """Repositório para operações com Pedido."""
    def __init__(self):
        super().__init__(Pedido)