import asyncio
import signal
import sys
import logging
from services.redis_service import RedisService

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('redis_receiver.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class RedisReceiver:
    def __init__(self, redis_host: str = "localhost", redis_port: int = 6379,
                 mongo_uri: str = "mongodb://localhost:27017"):
        """
        Inicializa o receptor Redis
        
        Args:
            redis_host: Host do Redis
            redis_port: Porta do Redis
            mongo_uri: URI de conexão com MongoDB
        """
        self.redis_service = RedisService(redis_host, redis_port, mongo_uri)
        self.running = False
        
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def signal_handler(self, signum, frame):
        """Handler para sinais de interrupção"""
        logger.info(f"Recebido sinal {signum}. Parando o serviço...")
        self.running = False
        self.redis_service.parar_escuta()
    
    async def iniciar(self):
        """Inicia o receptor Redis"""
        try:
            logger.info("Iniciando receptor Redis...")
            self.running = True
            
            await self.redis_service.iniciar_escuta()
            
        except KeyboardInterrupt:
            logger.info("Interrupção recebida. Parando o serviço...")
        except Exception as e:
            logger.error(f"Erro ao iniciar receptor Redis: {e}")
            raise
        finally:
            await self.parar()
    
    async def parar(self):
        """Para o receptor Redis"""
        logger.info("Parando receptor Redis...")
        self.running = False
        self.redis_service.parar_escuta()
        logger.info("Receptor Redis parado")

async def main():
    """Função principal"""
    redis_host = "localhost"
    redis_port = 6379
    mongo_uri = "mongodb://localhost:27017"
    
    receiver = RedisReceiver(redis_host, redis_port, mongo_uri)
    
    try:
        await receiver.iniciar()
    except Exception as e:
        logger.error(f"Erro fatal: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("RECEPTOR REDIS - Sincronização de Produtos")
    print("Canal monitorado:")
    print("- produtos: Eventos de produtos (CREATE, UPDATE, DELETE)")
    
    asyncio.run(main()) 