from beanie import Document
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Literal, Optional, List

class Envio(Document):
    endereco_entrega: str
    data_envio: Optional[datetime] = None
    status: Literal["preparando", "enviado", "entregue", "cancelado"] = "preparando"

    class Settings:
        name = "envios"

    def rastrear(self) -> str:
        status_messages = {
            "preparando": "Pedido sendo preparado para envio",
            "enviado": f"Enviado em {self.data_envio.strftime('%d/%m/%Y') if self.data_envio else 'N/A'}",
            "entregue": "Pedido entregue com sucesso",
            "cancelado": "Envio cancelado"
        }
        return status_messages.get(self.status, "Status desconhecido")