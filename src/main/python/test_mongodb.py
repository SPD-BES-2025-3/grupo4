import asyncio
import motor.motor_asyncio
from models.produto import Produto

async def test_mongodb():
    """Testa conexão com MongoDB"""
    try:
        # Conectar ao MongoDB
        client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
        
        # Testar conexão
        await client.admin.command('ping')
        print("Conectado ao MongoDB com sucesso")
        
        # Inicializar Beanie
        await Produto.init_beanie(database=client.ecommerce)
        print("Beanie inicializado com sucesso")

        # Listar produtos existentes
        produtos = await Produto.find_all().to_list()
        print(f"Produtos encontrados: {len(produtos)}")
        
        for produto in produtos:
            print(f"   - {produto.nome}: R$ {produto.preco:.2f}")
        
        client.close()
        
    except Exception as e:
        print(f"Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_mongodb()) 