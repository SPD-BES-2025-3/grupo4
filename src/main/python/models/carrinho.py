from beanie import Document
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Literal, Optional, List
from models.item_carrinho import ItemCarrinho
from models.produto import Produto

# Package Estoque
class Carrinho(Document):
    itens: List[ItemCarrinho] = Field(default_factory=list)
    total: float = 0.0

    class Settings:
        name = "carrinhos"

    def adicionar_item(self, produto: Produto, qtd: int) -> None:
        # Check if product already in cart
        for item in self.itens:
            if item.produto.id == produto.id:
                item.quantidade += qtd
                self.calcular_total()
                return
        
        # Add new item
        novo_item = ItemCarrinho(produto=produto, quantidade=qtd)
        self.itens.append(novo_item)
        self.calcular_total()

    def remover_item(self, produto: Produto) -> None:
        self.itens = [item for item in self.itens if item.produto.id != produto.id]
        self.calcular_total()

    def calcular_total(self) -> float:
        self.total = sum(item.subtotal() for item in self.itens)
        return self.total

    def esvaziar(self) -> None:
        self.itens.clear()
        self.total = 0.0