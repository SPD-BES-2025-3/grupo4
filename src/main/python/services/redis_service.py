import json
import asyncio
import logging
from typing import Dict, Any, Optional
from redis import Redis
from redis.exceptions import ConnectionError
import motor.motor_asyncio
from models.produto import Produto
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RedisService:
    def __init__(self, redis_host: str = "localhost", redis_port: int = 6379, 
                 mongo_uri: str = "mongodb://localhost:27017"):
        """
        Inicializa o serviço Redis para receber produtos do Java e sincronizar com MongoDB
        
        Args:
            redis_host: Host do Redis
            redis_port: Porta do Redis
            mongo_uri: URI de conexão com MongoDB
        """
        self.redis_client = Redis(host=redis_host, port=redis_port, decode_responses=True)
        self.mongo_client = motor.motor_asyncio.AsyncIOMotorClient(mongo_uri)
        self.db = self.mongo_client.ecommerce
        self.pubsub = None
        self.running = False
        
    async def conectar_mongodb(self):
        """Conecta ao MongoDB e inicializa as coleções"""
        try:
            # Testar conexão
            await self.mongo_client.admin.command('ping')
            logger.info("Conectado ao MongoDB com sucesso")
            
            # Inicializar Beanie com todos os modelos
            from models.produto import Produto
            from models.cliente import Cliente
            from models.carrinho import Carrinho
            from models.pedido import Pedido
            
            await Produto.init_beanie(database=self.mongo_client.ecommerce)
            await Cliente.init_beanie(database=self.mongo_client.ecommerce)
            await Carrinho.init_beanie(database=self.mongo_client.ecommerce)
            await Pedido.init_beanie(database=self.mongo_client.ecommerce)
            
        except Exception as e:
            logger.error(f"Erro ao conectar ao MongoDB: {e}")
            raise
    
    def conectar_redis(self):
        """Conecta ao Redis e configura os canais de escuta"""
        try:
            # Testar conexão
            self.redis_client.ping()
            logger.info("Conectado ao Redis com sucesso")
            
            # Configurar pubsub
            self.pubsub = self.redis_client.pubsub()
            
        except ConnectionError as e:
            logger.error(f"Erro ao conectar ao Redis: {e}")
            raise
    
    async def processar_evento_produto(self, dados: Dict[str, Any]):
        """
        Processa eventos de produtos vindos do Java
        
        Args:
            dados: Dados do evento contendo ação e produto
        """
        try:
            acao = dados.get("acao")
            produto_data = dados.get("produto")
            
            if not produto_data:
                logger.error("Dados do produto não encontrados no evento")
                return
            
            logger.info(f"Processando evento de produto: {acao} - {produto_data.get('nome', 'N/A')}")
            
            # Converter dados do Java para formato Python
            produto_mongo = {
                "nome": produto_data.get("nome"),
                "descricao": produto_data.get("descricao", ""),
                "preco": float(produto_data.get("preco", 0)),
                "estoque": int(produto_data.get("estoque", 0)),
                "categoria": produto_data.get("categoria", "Outros")
            }
            
            if acao == "CREATE":
                await self.criar_produto(produto_mongo)
            elif acao == "UPDATE":
                await self.atualizar_produto(produto_data.get("id"), produto_mongo)
            elif acao == "DELETE":
                await self.deletar_produto(produto_data.get("id"))
            else:
                logger.warning(f"Ação desconhecida: {acao}")
                
        except Exception as e:
            logger.error(f"Erro ao processar evento de produto: {e}")
    
    async def criar_produto(self, dados_produto: Dict[str, Any]):
        """Cria um novo produto no MongoDB"""
        try:
            # Verificar se produto já existe
            produto_existente = await Produto.find_one({"nome": dados_produto["nome"]})
            if produto_existente:
                logger.warning(f"Produto já existe: {dados_produto['nome']}")
                return
            
            produto = Produto(**dados_produto)
            await produto.insert()
            logger.info(f"Produto criado com sucesso: {produto.nome}")
        except Exception as e:
            logger.error(f"Erro ao criar produto: {e}")
    
    async def atualizar_produto(self, produto_id: int, dados_produto: Dict[str, Any]):
        """Atualiza um produto existente no MongoDB"""
        try:
            # Buscar produto por nome
            produto = await Produto.find_one({"nome": dados_produto["nome"]})
            if produto:
                for key, value in dados_produto.items():
                    setattr(produto, key, value)
                await produto.save()
                logger.info(f"Produto atualizado com sucesso: {produto.nome}")
            else:
                logger.warning(f"Produto não encontrado para atualização: {dados_produto['nome']}")
                # Criar produto se não existir
                await self.criar_produto(dados_produto)
        except Exception as e:
            logger.error(f"Erro ao atualizar produto: {e}")
    
    async def deletar_produto(self, produto_id: int):
        """Deleta um produto do MongoDB"""
        try:
            produtos = await Produto.find_all().to_list()
            produto_para_deletar = None
            
            for produto in produtos:
                if str(produto_id) in produto.nome:
                    produto_para_deletar = produto
                    break
            
            if produto_para_deletar:
                await produto_para_deletar.delete()
                logger.info(f"Produto deletado com sucesso: {produto_para_deletar.nome}")
            else:
                logger.warning(f"Produto não encontrado para deleção: {produto_id}")
        except Exception as e:
            logger.error(f"Erro ao deletar produto: {e}")
    
    def callback_produtos(self, message):
        """Callback para mensagens do canal 'produtos'"""
        try:
            dados = json.loads(message['data'])
            asyncio.create_task(self.processar_evento_produto(dados))
        except Exception as e:
            logger.error(f"Erro no callback de produtos: {e}")
    
    async def iniciar_escuta(self):
        """Inicia a escuta dos canais Redis"""
        try:
            # Conectar ao Redis
            self.conectar_redis()
            
            # Conectar ao MongoDB
            await self.conectar_mongodb()
            
            # Configurar canal de escuta apenas para produtos
            self.pubsub.subscribe(produtos=self.callback_produtos)
            
            self.running = True
            logger.info("Iniciando escuta do canal 'produtos' no Redis...")
            
            # Iniciar loop de escuta
            for message in self.pubsub.listen():
                if not self.running:
                    break
                    
                if message['type'] == 'message' and message['channel'] == 'produtos':
                    self.callback_produtos(message)
                        
        except Exception as e:
            logger.error(f"Erro ao iniciar escuta Redis: {e}")
            raise
    
    def parar_escuta(self):
        """Para a escuta dos canais Redis"""
        self.running = False
        if self.pubsub:
            self.pubsub.unsubscribe()
            self.pubsub.close()
        logger.info("Escuta Redis parada")
    
    def __del__(self):
        """Cleanup ao destruir o objeto"""
        self.parar_escuta()
        if hasattr(self, 'redis_client'):
            self.redis_client.close()
        if hasattr(self, 'mongo_client'):
            self.mongo_client.close() 