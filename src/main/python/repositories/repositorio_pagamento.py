from repositories import RepositorioBase, RedisCache
from models.pagamento import Pagamento
from typing import List

class RepositorioPagamento(RepositorioBase[Pagamento]):
    """Repositório específico para operações com pagamentos.
    
    Herda operações CRUD básicas do RepositorioBase e adiciona
    funcionalidades específicas para o modelo Pagamento.
    """
    
    def __init__(self, cache: RedisCache | None = None):
        """Inicializa o repositório de pagamentos com cache opcional."""
        super().__init__(Pagamento, cache)
    
    # Funções utilitárias específicas para pagamentos
    async def buscar_pagamentos_por_status(self, status: str) -> List[Pagamento]:
        return await self.modelo.find(self.modelo.status == status).to_list()
    
    async def buscar_pagamentos_por_metodo(self, metodo: str) -> List[Pagamento]:
        return await self.modelo.find(self.modelo.metodo == metodo).to_list()
    
    async def buscar_pagamentos_por_valor_minimo(self, valor_minimo: float) -> List[Pagamento]:
        return await self.modelo.find(self.modelo.valor >= valor_minimo).to_list()
    
    async def contar_total_pagamentos(self) -> int:
        return await self.modelo.count()
    
    async def contar_pagamentos_por_status(self, status: str) -> int:
        return await self.modelo.find(self.modelo.status == status).count()
    
    async def buscar_pagamentos_por_faixa_valor(self, valor_minimo: float, valor_maximo: float) -> List[Pagamento]:
        return await self.modelo.find(
            self.modelo.valor >= valor_minimo,
            self.modelo.valor <= valor_maximo
        ).to_list()
    
    async def verificar_pagamento_existe(self, id: str) -> bool:
        if not self.eh_object_id_valido(id):
            return False
        try:
            pagamento = await self.modelo.get(id)
            return pagamento is not None
        except Exception:
            return False
