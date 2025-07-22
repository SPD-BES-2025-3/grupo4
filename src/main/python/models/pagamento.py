from beanie import Document
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Literal

class Pagamento(Document):
    dados_pagamento: str
    valor: float
    metodo: Literal["cartao", "boleto", "pix", "paypal"]  # you can expand this
    status: Literal["pendente", "processado", "falhou"] = "pendente"

    class Settings:
        name = "pagamentos"  # MongoDB collection name

    def processar(self) -> bool:
        # Simulate payment processing logic
        if self.status != "pendente":
            return False
        # Add logic to interact with payment gateway
        self.status = "processado"
        return True

    def __str__(self) -> str:
        return (f"{self.id}: Pagamento: R$ {self.valor:.2f} via {self.metodo} "
                f"({self.status}) - {self.dados_pagamento}")