from repositories.repositorio_base import RepositorioBase
from models.item_pedido import ItemPedido

class RepositorioItemPedido(RepositorioBase[ItemPedido]):
    """Repositório para operações com ItemPedido."""
    def __init__(self):
        super().__init__(ItemPedido)