#!/usr/bin/env python3
"""
Script de teste para verificar conexão Redis e receber mensagens
"""

import redis
import json
import time

def test_redis_connection():
    """Testa conexão com Redis e recebe mensagens"""
    try:
        # Conectar ao Redis
        r = redis.Redis(host='localhost', port=6379, decode_responses=True)
        
        # Testar conexão
        r.ping()
        print("Conectado ao Redis com sucesso")
        
        # Configurar pubsub
        pubsub = r.pubsub()
        pubsub.subscribe('produtos')
        
        print("Escutando canal 'produtos'...")
        print("Pressione Ctrl+C para parar")
        
        # Escutar mensagens
        for message in pubsub.listen():
            if message['type'] == 'message':
                print(f"📨 Mensagem recebida: {message['data']}")
                try:
                    data = json.loads(message['data'])
                    print(f"   Ação: {data.get('acao')}")
                    print(f"   Produto: {data.get('produto', {}).get('nome', 'N/A')}")
                except json.JSONDecodeError as e:
                    print(f"   Erro ao decodificar JSON: {e}")
        
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    test_redis_connection() 