from beanie import Document
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Literal, Optional, List

# Package Estoque
class Produto(Document):
    nome: str
    descricao: str
    preco: float
    estoque: int
    categoria: str

    class Settings:
        name = "produtos"

    def atualizar_estoque(self, qtd: int) -> None:
        self.estoque += qtd
        if self.estoque < 0:
            self.estoque = 0

    def aplicar_desconto(self, percentual: float) -> None:
        if 0 <= percentual <= 100:
            self.preco = self.preco * (1 - percentual / 100)

    def __str__(self) -> str:
        return f"{self.nome} - R$ {self.preco:.2f} (Estoque: {self.estoque})"