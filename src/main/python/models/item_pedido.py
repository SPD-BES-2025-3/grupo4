from pydantic import BaseModel, Field
from models.produto import Produto

class ItemPedido(BaseModel):
    produto: Produto
    quantidade: int = Field(..., ge=1)
    preco_unitario: float = Field(..., gt=0)

    def subtotal(self) -> float:
        return self.quantidade * self.preco_unitario

    def __str__(self) -> str:
        return (
            f"{self.quantidade} x {self.produto.nome} "
            f"@ R$ {self.preco_unitario:.2f} = R$ {self.subtotal():.2f}"
        )
