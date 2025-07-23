from __future__ import annotations
from beanie import Document
from typing import Optional

class Cliente(Document):
    nome: str
    email: str
    senha: str
    endereco: str
    logado: bool = False

    class Settings:
        name = "clientes"

    def login(self) -> bool:
        self.logado = True
        return True

    def logout(self) -> None:
        self.logado = False

    def atualizar_perfil(self, nome: Optional[str] = None, email: Optional[str] = None, endereco: Optional[str] = None) -> None:
        if nome:
            self.nome = nome
        if email:
            self.email = email
        if endereco:
            self.endereco = endereco

    async def adicionar_ao_carrinho(self, produto: 'Produto') -> 'Carrinho':
        from models.carrinho import Carrinho
        carrinho = await Carrinho.find_one({"cliente_id": str(self.id)})
        if not carrinho:
            carrinho = Carrinho()
            carrinho.cliente_id = str(self.id)

        carrinho.adicionar_item(produto, 1)
        await carrinho.save()
        return carrinho

    async def fazer_pedido(self) -> 'Pedido':
        from models.pedido import Pedido
        from models.carrinho import Carrinho

        carrinho = await Carrinho.find_one({"cliente_id": str(self.id)})
        if not carrinho:
            raise ValueError("Carrinho não encontrado")
        if not carrinho.itens:
            raise ValueError("Carrinho está vazio")

        pedido = await Pedido.criar_a_partir_do_carrinho(self, carrinho)

        carrinho.esvaziar()
        await carrinho.save()

        await pedido.insert()

        return pedido
