from repositories.repositorio_base import RepositorioBase
from models.item_carrinho import ItemCarrinho

class RepositorioItemCarrinho(RepositorioBase[ItemCarrinho]):
    """Repositório para operações com ItemCarrinho."""
    def __init__(self):
        super().__init__(ItemCarrinho)