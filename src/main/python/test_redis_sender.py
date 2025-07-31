#!/usr/bin/env python3
"""
Script de teste para simular o envio de produtos do Java via Redis
"""

import json
import time
from redis import Redis

def simular_envio_produto():
    """Simula o envio de produtos do Java para o Redis"""
    
    redis_client = Redis(host="localhost", port=6379, decode_responses=True)
    
    produtos_teste = [
        {
            "acao": "CREATE",
            "produto": {
                "id": 1,
                "nome": "Notebook Dell Inspiron",
                "descricao": "Notebook Dell Inspiron 15 polegadas, 8GB RAM, 256GB SSD",
                "preco": 2999.99,
                "estoque": 10,
                "categoria": "Informática"
            }
        },
        {
            "acao": "CREATE",
            "produto": {
                "id": 2,
                "nome": "Smartphone Samsung Galaxy",
                "descricao": "Smartphone Samsung Galaxy S21, 128GB, Preto",
                "preco": 3999.99,
                "estoque": 25,
                "categoria": "Smartphones"
            }
        },
        {
            "acao": "CREATE",
            "produto": {
                "id": 3,
                "nome": "Mouse USB Logitech",
                "descricao": "Mouse USB Logitech M185, Sem Fio, Preto",
                "preco": 29.99,
                "estoque": 50,
                "categoria": "Informática"
            }
        },
        {
            "acao": "UPDATE",
            "produto": {
                "id": 1,
                "nome": "Notebook Dell Inspiron",
                "descricao": "Notebook Dell Inspiron 15 polegadas, 16GB RAM, 512GB SSD",
                "preco": 3499.99,
                "estoque": 8,
                "categoria": "Informática"
            }
        },
        {
            "acao": "DELETE",
            "produto": {
                "id": 3,
                "nome": "Mouse USB Logitech",
                "descricao": "Mouse USB Logitech M185, Sem Fio, Preto",
                "preco": 29.99,
                "estoque": 50,
                "categoria": "Informática"
            }
        }
    ]
    
    print("=" * 60)
    print("SIMULADOR DE ENVIO DE PRODUTOS VIA REDIS")
    print("Simulando dados vindos do Java (PostgreSQL)")
    print("=" * 60)
    
    try:
        redis_client.ping()
        
        for i, produto in enumerate(produtos_teste, 1):
            json_data = json.dumps(produto)
            redis_client.publish("produtos", json_data)
            
            print(f"   Enviado produto {i}/{len(produtos_teste)}:")
            print(f"   Ação: {produto['acao']}")
            print(f"   Nome: {produto['produto']['nome']}")
            print(f"   Preço: R$ {produto['produto']['preco']:.2f}")
            print(f"   Estoque: {produto['produto']['estoque']}")
            print()
            time.sleep(2)
        
        print("Todos os produtos foram enviados com sucesso!")
        
    except Exception as e:
        print(f"Erro ao enviar produtos: {e}")
    finally:
        redis_client.close()

if __name__ == "__main__":
    simular_envio_produto() 