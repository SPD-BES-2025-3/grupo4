#!/usr/bin/env python3
"""
Receptor Redis com debug para identificar problemas
"""

import redis
import json
import asyncio
import motor.motor_asyncio
from datetime import datetime

class RedisReceiverDebug:
    def __init__(self):
        self.redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)
        self.mongo_client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
        self.db = self.mongo_client.ecommerce
        self.running = True
    
    def test_redis_connection(self):
        """Testa conexão com Redis"""
        try:
            self.redis_client.ping()
            print("Redis conectado com sucesso")
            return True
        except Exception as e:
            print(f"Erro ao conectar ao Redis: {e}")
            return False
    
    async def test_mongo_connection(self):
        """Testa conexão com MongoDB"""
        try:
            await self.mongo_client.admin.command('ping')
            print("MongoDB conectado com sucesso")
            return True
        except Exception as e:
            print(f"Erro ao conectar ao MongoDB: {e}")
            return False
    
    def listen_redis(self):
        """Escuta mensagens do Redis"""
        try:
            pubsub = self.redis_client.pubsub()
            pubsub.subscribe('produtos')
            
            print("Escutando canal 'produtos'...")
            print("Pressione Ctrl+C para parar")
            
            for message in pubsub.listen():
                if not self.running:
                    break
                
                if message['type'] == 'message':
                    print(f"📨 Mensagem recebida: {message['data']}")
                    try:
                        data = json.loads(message['data'])
                        print(f"   Ação: {data.get('acao')}")
                        print(f"   Produto: {data.get('produto', {}).get('nome', 'N/A')}")
                        
                        # Processar a mensagem (executar em thread separada)
                        import threading
                        def process_async():
                            loop = asyncio.new_event_loop()
                            asyncio.set_event_loop(loop)
                            try:
                                loop.run_until_complete(self.process_message(data))
                            finally:
                                loop.close()
                        
                        thread = threading.Thread(target=process_async)
                        thread.daemon = True
                        thread.start()
                        
                    except json.JSONDecodeError as e:
                        print(f"   Erro ao decodificar JSON: {e}")
                    except Exception as e:
                        print(f"   Erro ao processar mensagem: {e}")
        
        except Exception as e:
            print(f"Erro ao escutar Redis: {e}")
    
    async def process_message(self, data):
        """Processa mensagem recebida"""
        try:
            acao = data.get('acao')
            produto_data = data.get('produto')
            
            if not produto_data:
                print("   Dados do produto não encontrados")
                return
            
            print(f"Processando: {acao} - {produto_data.get('nome')}")
            
            # Preparar dados para MongoDB
            produto_mongo = {
                "nome": produto_data.get("nome"),
                "descricao": produto_data.get("descricao", ""),
                "preco": float(produto_data.get("preco", 0)),
                "estoque": int(produto_data.get("estoque", 0)),
                "categoria": produto_data.get("categoria", "Outros"),
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            }
            
            if acao in ["CREATE", "criado"]:
                await self.criar_produto(produto_mongo)
            elif acao in ["UPDATE", "atualizado"]:
                await self.atualizar_produto(produto_data.get("id"), produto_mongo)
            elif acao in ["DELETE", "removido"]:
                await self.deletar_produto(produto_data.get("id"))
            else:
                print(f"   Ação desconhecida: {acao}")
                
        except Exception as e:
            print(f"   Erro ao processar mensagem: {e}")
    
    async def criar_produto(self, dados_produto):
        """Cria produto no MongoDB"""
        try:
            # Verificar se já existe
            existente = await self.db.produtos.find_one({"nome": dados_produto["nome"]})
            if existente:
                print(f"   Produto já existe: {dados_produto['nome']}")
                return
            
            # Inserir produto
            result = await self.db.produtos.insert_one(dados_produto)
            print(f"   Produto criado: {dados_produto['nome']} (ID: {result.inserted_id})")
            
        except Exception as e:
            print(f"   Erro ao criar produto: {e}")
    
    async def atualizar_produto(self, produto_id, dados_produto):
        """Atualiza produto no MongoDB"""
        try:
            dados_produto["updated_at"] = datetime.now()
            result = await self.db.produtos.update_one(
                {"nome": dados_produto["nome"]}, 
                {"$set": dados_produto}
            )
            print(f"   Produto atualizado: {dados_produto['nome']}")
            
        except Exception as e:
            print(f"   Erro ao atualizar produto: {e}")
    
    async def deletar_produto(self, produto_id):
        """Deleta produto do MongoDB"""
        try:
            # Buscar por nome (assumindo que contém o ID)
            produtos = await self.db.produtos.find().to_list(None)
            produto_para_deletar = None
            
            for produto in produtos:
                if str(produto_id) in produto.get("nome", ""):
                    produto_para_deletar = produto
                    break
            
            if produto_para_deletar:
                await self.db.produtos.delete_one({"_id": produto_para_deletar["_id"]})
                print(f"   Produto deletado: {produto_para_deletar['nome']}")
            else:
                print(f"   Produto não encontrado para deleção: {produto_id}")
                
        except Exception as e:
            print(f"   Erro ao deletar produto: {e}")
    
    def stop(self):
        """Para o receptor"""
        self.running = False
        self.redis_client.close()
        self.mongo_client.close()

async def main():
    """Função principal"""
    receiver = RedisReceiverDebug()
    
    # Testar conexões
    if not receiver.test_redis_connection():
        return
    
    if not await receiver.test_mongo_connection():
        return
    
    print(" Iniciando receptor Redis...")
    
    try:
        # Executar em thread separada
        import threading
        redis_thread = threading.Thread(target=receiver.listen_redis)
        redis_thread.daemon = True
        redis_thread.start()
        
        # Manter vivo
        while receiver.running:
            await asyncio.sleep(1)
            
    except KeyboardInterrupt:
        print("\nParando receptor...")
        receiver.stop()

if __name__ == "__main__":
    print("=" * 60)
    print("RECEPTOR REDIS DEBUG - Sincronização de Produtos")
    print("PostgreSQL (Java) -> MongoDB (Python)")
    print("=" * 60)
    
    asyncio.run(main()) 