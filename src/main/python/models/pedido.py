from __future__ import annotations
from beanie import Document
from pydantic import Field
from datetime import datetime
from typing import Literal, Optional, List

class Pedido(Document):
    data_pedido: datetime = Field(default_factory=datetime.now)
    status: Literal["pendente", "confirmado", "enviado", "entregue", "cancelado"] = "pendente"
    total: float
    cliente: 'Cliente'  # string aqui evita import circular
    itens: List['ItemPedido'] = Field(default_factory=list)
    pagamento: Optional['Pagamento'] = None
    envio: Optional['Envio'] = None

    class Settings:
        name = "pedidos"

    def cancelar(self) -> None:
        if self.status != "entregue":
            self.status = "cancelado"

    def atualizar_status(self, novo_status: Literal["pendente", "confirmado", "enviado", "entregue", "cancelado"]) -> None:
        self.status = novo_status

    @classmethod
    async def criar_a_partir_do_carrinho(cls, cliente: Cliente, carrinho: 'Carrinho') -> Pedido:
        # Importar aqui para evitar import circular
        from models.item_pedido import ItemPedido

        if not carrinho.itens:
            raise ValueError("Carrinho está vazio")

        itens_pedido = [
            ItemPedido(
                id=item.id,
                produto=item.produto,
                quantidade=item.quantidade,
                preco_unitario=item.produto.preco
            )
            for item in carrinho.itens
        ]

        total = sum(item.subtotal() for item in itens_pedido)

        pedido = cls(
            cliente=cliente,
            total=total,
            itens=itens_pedido
        )

        return pedido

    def __str__(self) -> str:
        return f"{self.id}: Pedido de R$ {self.total:.2f} - {self.status} ({self.data_pedido.strftime('%d/%m/%Y')})"
