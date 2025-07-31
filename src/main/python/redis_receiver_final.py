#!/usr/bin/env python3
"""
Receptor Redis Final - Sincronização de Produtos
PostgreSQL (Java) -> MongoDB (Python)
"""

import redis
import json
import motor.motor_asyncio
import asyncio
import threading
from datetime import datetime

class RedisReceiverFinal:
    def __init__(self):
        self.redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)
        self.mongo_client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
        self.db = self.mongo_client.ecommerce
        self.running = True
    
    def test_connections(self):
        """Testa conexões com Redis e MongoDB"""
        try:
            # Testar Redis
            self.redis_client.ping()
            print("Redis conectado com sucesso")
            
            # Testar MongoDB (síncrono)
            import pymongo
            mongo_client = pymongo.MongoClient("mongodb://localhost:27017")
            mongo_client.admin.command('ping')
            print("MongoDB conectado com sucesso")
            mongo_client.close()
            
            return True
        except Exception as e:
            print(f"Erro de conexão: {e}")
            return False
    
    def listen_redis(self):
        """Escuta mensagens do Redis"""
        try:
            pubsub = self.redis_client.pubsub()
            pubsub.subscribe('produtos')
            
            print("🔍 Escutando canal 'produtos'...")
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
                        
                        # Processar mensagem em thread separada
                        self.process_message_sync(data)
                        
                    except json.JSONDecodeError as e:
                        print(f"   Erro ao decodificar JSON: {e}")
                    except Exception as e:
                        print(f"   Erro ao processar mensagem: {e}")
        
        except Exception as e:
            print(f"Erro ao escutar Redis: {e}")
    
    def process_message_sync(self, data):
        """Processa mensagem de forma síncrona"""
        try:
            acao = data.get('acao')
            produto_data = data.get('produto')
            
            if not produto_data:
                print("   Dados do produto não encontrados")
                return
            
            print(f"   🔄 Processando: {acao} - {produto_data.get('nome')}")
            
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
                self.criar_produto_sync(produto_mongo)
            elif acao in ["UPDATE", "atualizado"]:
                self.atualizar_produto_sync(produto_data.get("id"), produto_mongo)
            elif acao in ["DELETE", "removido"]:
                self.deletar_produto_sync(produto_data.get("id"))
            else:
                print(f"   ⚠️ Ação desconhecida: {acao}")
                
        except Exception as e:
            print(f"   Erro ao processar mensagem: {e}")
    
    def criar_produto_sync(self, dados_produto):
        """Cria produto no MongoDB de forma síncrona"""
        try:
            import pymongo
            mongo_client = pymongo.MongoClient("mongodb://localhost:27017")
            db = mongo_client.ecommerce
            
            # Verificar se já existe
            existente = db.produtos.find_one({"nome": dados_produto["nome"]})
            if existente:
                print(f"   ⚠️ Produto já existe: {dados_produto['nome']}")
                mongo_client.close()
                return
            
            # Inserir produto
            result = db.produtos.insert_one(dados_produto)
            print(f"   Produto criado: {dados_produto['nome']} (ID: {result.inserted_id})")
            
            mongo_client.close()
            
        except Exception as e:
            print(f"   Erro ao criar produto: {e}")
    
    def atualizar_produto_sync(self, produto_id, dados_produto):
        """Atualiza produto no MongoDB de forma síncrona"""
        try:
            import pymongo
            mongo_client = pymongo.MongoClient("mongodb://localhost:27017")
            db = mongo_client.ecommerce
            
            dados_produto["updated_at"] = datetime.now()
            result = db.produtos.update_one(
                {"nome": dados_produto["nome"]}, 
                {"$set": dados_produto}
            )
            print(f"   Produto atualizado: {dados_produto['nome']}")
            
            mongo_client.close()
            
        except Exception as e:
            print(f"   Erro ao atualizar produto: {e}")
    
    def deletar_produto_sync(self, produto_id):
        """Deleta produto do MongoDB de forma síncrona"""
        try:
            import pymongo
            mongo_client = pymongo.MongoClient("mongodb://localhost:27017")
            db = mongo_client.ecommerce
            
            # Buscar por nome (assumindo que contém o ID)
            produtos = list(db.produtos.find())
            produto_para_deletar = None
            
            for produto in produtos:
                if str(produto_id) in produto.get("nome", ""):
                    produto_para_deletar = produto
                    break
            
            if produto_para_deletar:
                db.produtos.delete_one({"_id": produto_para_deletar["_id"]})
                print(f"   Produto deletado: {produto_para_deletar['nome']}")
            else:
                print(f"   ⚠️ Produto não encontrado para deleção: {produto_id}")
            
            mongo_client.close()
                
        except Exception as e:
            print(f"   Erro ao deletar produto: {e}")
    
    def stop(self):
        """Para o receptor"""
        self.running = False
        self.redis_client.close()
        self.mongo_client.close()

def main():
    """Função principal"""
    receiver = RedisReceiverFinal()
    
    # Testar conexões
    if not receiver.test_connections():
        return
    
    print("🚀 Iniciando receptor Redis...")
    
    try:
        # Escutar Redis
        receiver.listen_redis()
            
    except KeyboardInterrupt:
        print("\n🛑 Parando receptor...")
        receiver.stop()

if __name__ == "__main__":
    print("=" * 60)
    print("RECEPTOR REDIS FINAL - Sincronização de Produtos")
    print("PostgreSQL (Java) -> MongoDB (Python)")
    print("=" * 60)
    
    main() 