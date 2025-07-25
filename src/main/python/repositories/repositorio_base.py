from typing import TypeVar, Generic, Optional, Dict, Any, Type
from config.redis_cache import RedisCache
from beanie import Document

T = TypeVar('T', bound=Document)

class RepositorioBase(Generic[T]):
    """Repositório genérico para operações CRUD com Beanie/MongoDB.
    
    Esta classe fornece operações básicas de CRUD que podem ser reutilizadas
    para qualquer modelo que herde de Document do Beanie.
    """
    
    def __init__(self, modelo: Type[T], cache: Optional[RedisCache] = None):
        """Inicializa o repositório com o modelo especificado.
        
        Args:
            modelo (Type[T]): Classe do modelo que herda de Document.
        """
        self.modelo = modelo
        self.cache = cache
    
    def eh_object_id_valido(self, id_string: str) -> bool:
        """Verifica se a string é um formato válido de ObjectId do MongoDB.
        
        Args:
            id_string (str): String a ser validada como ObjectId.
            
        Returns:
            bool: True se for um ObjectId válido, False caso contrário.
        """
        if not isinstance(id_string, str) or len(id_string) != 24:
            return False
        try:
            int(id_string, 16)  # Verifica se é hexadecimal válido
            return True
        except ValueError:
            return False
    
    async def criar(self, entidade: T) -> T:
        """Cria uma nova entidade no banco de dados.
        
        Args:
            entidade (T): Objeto da entidade a ser criada.
            
        Returns:
            T: A entidade criada com ID atribuído.
        """
        await entidade.insert()
        return entidade
    
    async def buscar_por_id(self, id: str) -> Optional[T]:
        if not self.eh_object_id_valido(id):
            return None

        if self.cache:
            cached = await self.cache.get(f"{self.modelo.__name__}:{id}")
            if cached:
                self.modelo.model_validate_json(cached)

        try:
            entidade = await self.modelo.get(id)
            if entidade and self.cache:
                await self.cache.set(f"{self.modelo.__name__}:{id}", entidade.model_dump_json())
            return entidade
        except Exception:
            return None
    
    async def listar_todos(self) -> list[T]:
        """Lista todas as entidades do banco de dados.
        
        Returns:
            list[T]: Lista com todas as entidades encontradas.
        """
        return await self.modelo.find_all().to_list()
    
    async def atualizar_por_id(self, id: str, dados_atualizacao: Dict[str, Any]) -> Optional[T]:
        entidade = await self.buscar_por_id(id)
        if not entidade:
            return None
        await entidade.set(dados_atualizacao)
        if self.cache:
            await self.cache.set(f"{self.modelo.__name__}:{id}", entidade.model_dump_json())
        return entidade
    
    async def atualizar_completo(self, entidade: T) -> Optional[T]:
        """Atualiza um objeto de entidade completo.
        
        Args:
            entidade (T): Objeto da entidade com as alterações a serem salvas.
            
        Returns:
            Optional[T]: A entidade atualizada ou None se não encontrada.
        """
        if not entidade.id:
            return None
        
        entidade_existente = await self.modelo.get(entidade.id)
        if not entidade_existente:
            return None
        
        await entidade.save()
        return entidade
    
    async def deletar_por_id(self, id: str) -> bool:
        entidade = await self.buscar_por_id(id)
        if not entidade:
            return False
        await entidade.delete()
        if self.cache:
            await self.cache.delete(f"{self.modelo.__name__}:{id}")
        return True
    
    async def deletar_por_objeto(self, entidade: T) -> bool:
        """Deleta um objeto de entidade.
        
        Args:
            entidade (T): Objeto da entidade a ser deletada.
            
        Returns:
            bool: True se deletada com sucesso, False caso contrário.
        """
        if not entidade.id:
            return False
        
        await entidade.delete()
        return True
    
    async def contar_total(self) -> int:
        """Conta o número total de entidades no banco de dados.
        
        Returns:
            int: Número total de entidades.
        """
        return await self.modelo.count()
    
    async def verificar_existe(self, id: str) -> bool:
        """Verifica se uma entidade existe pelo ID.
        
        Args:
            id (str): ID da entidade a ser verificada.
            
        Returns:
            bool: True se a entidade existe, False caso contrário.
        """
        if not self.eh_object_id_valido(id):
            return False
        
        try:
            entidade = await self.modelo.get(id)
            return entidade is not None
        except Exception:
            return False
