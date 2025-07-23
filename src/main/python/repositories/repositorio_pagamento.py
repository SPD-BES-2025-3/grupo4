# repositories/repositorio_pagamento.py

from repositories.repositorio_base import RepositorioBase
from models.pagamento import Pagamento
from typing import List

class RepositorioPagamento(RepositorioBase[Pagamento]):
    """Repositório específico para operações com pagamentos.
    
    Herda operações CRUD básicas do RepositorioBase e adiciona
    funcionalidades específicas para o modelo Pagamento.
    """
    
    def __init__(self):
        """Inicializa o repositório de pagamentos."""
        super().__init__(Pagamento)
    
    # Funções utilitárias específicas para pagamentos (mantendo nomes originais)
    async def buscar_pagamentos_por_status(self, status: str) -> List[Pagamento]:
        """Busca pagamentos por status específico.
        
        Args:
            status (str): Status dos pagamentos a serem buscados.
            
        Returns:
            List[Pagamento]: Lista de pagamentos com o status especificado.
        """
        return await self.modelo.find(self.modelo.status == status).to_list()
    
    async def buscar_pagamentos_por_metodo(self, metodo: str) -> List[Pagamento]:
        """Busca pagamentos por método de pagamento.
        
        Args:
            metodo (str): Método de pagamento a ser filtrado.
            
        Returns:
            List[Pagamento]: Lista de pagamentos com o método especificado.
        """
        return await self.modelo.find(self.modelo.metodo == metodo).to_list()
    
    async def buscar_pagamentos_por_valor_minimo(self, valor_minimo: float) -> List[Pagamento]:
        """Busca pagamentos com valor maior ou igual ao mínimo especificado.
        
        Args:
            valor_minimo (float): Valor mínimo para filtrar os pagamentos.
            
        Returns:
            List[Pagamento]: Lista de pagamentos com valor >= valor_minimo.
        """
        return await self.modelo.find(self.modelo.valor >= valor_minimo).to_list()
    
    async def contar_total_pagamentos(self) -> int:
        """Conta o número total de pagamentos no banco de dados.
        
        Returns:
            int: Número total de pagamentos.
        """
        return await self.modelo.count()
    
    async def contar_pagamentos_por_status(self, status: str) -> int:
        """Conta pagamentos por status específico.
        
        Args:
            status (str): Status dos pagamentos a serem contados.
            
        Returns:
            int: Número de pagamentos com o status especificado.
        """
        return await self.modelo.find(self.modelo.status == status).count()
    
    async def buscar_pagamentos_por_faixa_valor(self, valor_minimo: float, valor_maximo: float) -> List[Pagamento]:
        """Busca pagamentos dentro de uma faixa de valores.
        
        Args:
            valor_minimo (float): Valor mínimo da faixa.
            valor_maximo (float): Valor máximo da faixa.
            
        Returns:
            List[Pagamento]: Lista de pagamentos dentro da faixa especificada.
        """
        return await self.modelo.find(
            self.modelo.valor >= valor_minimo,
            self.modelo.valor <= valor_maximo
        ).to_list()
    
    async def verificar_pagamento_existe(self, id: str) -> bool:
        """Verifica se um pagamento existe pelo ID.
        
        Args:
            id (str): ID do pagamento a ser verificado.
            
        Returns:
            bool: True se o pagamento existe, False caso contrário.
        """
        if not self.eh_object_id_valido(id):
            return False
        
        try:
            pagamento = await self.modelo.get(id)
            return pagamento is not None
        except Exception:
            return False