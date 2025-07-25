import asyncio
from config.redis_cache import RedisCache

async def testar_redis():
    cache = RedisCache(host="localhost", port=6379, db=1)
    await cache.set("produto:test", '{"nome": "Caneca", "preco": 29.9}')
    resultado = await cache.get("produto:test")
    print("Valor no cache:", resultado)

asyncio.run(testar_redis())
