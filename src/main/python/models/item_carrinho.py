from beanie import Document
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Literal, Optional, List
from models.produto import Produto

class ItemCarrinho(BaseModel):
    produto: Produto
    quantidade: int

    def subtotal(self) -> float:
        return self.produto.preco * self.quantidade