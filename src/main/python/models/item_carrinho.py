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
    
    def __str__(self) -> str:
        return f"{self.quantidade} x {self.produto.nome} (R$ {self.subtotal():.2f})"
