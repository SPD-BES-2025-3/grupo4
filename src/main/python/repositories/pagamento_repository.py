# repositories/pagamento_repository.py

from models.pagamento import Pagamento
from typing import Optional, Dict, Any
from beanie import PydanticObjectId

def is_valid_object_id(id_string: str) -> bool:
    """Check if string is a valid MongoDB ObjectId format"""
    if not isinstance(id_string, str) or len(id_string) != 24:
        return False
    try:
        int(id_string, 16)  # Check if it's valid hexadecimal
        return True
    except ValueError:
        return False

async def criar_pagamento(pagamento: Pagamento) -> Pagamento:
    """Create a new payment"""
    await pagamento.insert()
    return pagamento

async def buscar_pagamento(id: str) -> Pagamento | None:
    """Find a payment by ID with validation"""
    if not is_valid_object_id(id):
        return None
    
    try:
        return await Pagamento.get(id)
    except Exception:
        return None

async def listar_pagamentos() -> list[Pagamento]:
    """List all payments"""
    return await Pagamento.find_all().to_list()

async def atualizar_pagamento(id: str, dados_atualizacao: Dict[str, Any]) -> Pagamento | None:
    """Update a payment by ID with provided data"""
    if not is_valid_object_id(id):
        return None
    
    try:
        pagamento = await Pagamento.get(id)
        if not pagamento:
            return None
        
        # Update the document with new data
        await pagamento.set(dados_atualizacao)
        return pagamento
    except Exception:
        return None

async def atualizar_pagamento_completo(pagamento: Pagamento) -> Pagamento | None:
    """Update a complete payment object"""
    if not pagamento.id:
        return None
    
    existing = await Pagamento.get(pagamento.id)
    if not existing:
        return None
    
    await pagamento.save()
    return pagamento

async def deletar_pagamento(id: str) -> bool:
    """Delete a payment by ID with validation"""
    if not is_valid_object_id(id):
        return False
    
    try:
        pagamento = await Pagamento.get(id)
        if not pagamento:
            return False
        
        await pagamento.delete()
        return True
    except Exception:
        return False

async def deletar_pagamento_objeto(pagamento: Pagamento) -> bool:
    """Delete a payment object"""
    if not pagamento.id:
        return False
    
    await pagamento.delete()
    return True

# Additional utility functions
async def buscar_pagamentos_por_status(status: str) -> list[Pagamento]:
    """Find payments by status"""
    return await Pagamento.find(Pagamento.status == status).to_list()

async def buscar_pagamentos_por_metodo(metodo: str) -> list[Pagamento]:
    """Find payments by method"""
    return await Pagamento.find(Pagamento.metodo == metodo).to_list()

async def buscar_pagamentos_por_valor_minimo(valor_minimo: float) -> list[Pagamento]:
    """Find payments with value greater than or equal to minimum"""
    return await Pagamento.find(Pagamento.valor >= valor_minimo).to_list()

async def contar_pagamentos() -> int:
    """Count total number of payments"""
    return await Pagamento.count()

async def contar_pagamentos_por_status(status: str) -> int:
    """Count payments by status"""
    return await Pagamento.find(Pagamento.status == status).count()