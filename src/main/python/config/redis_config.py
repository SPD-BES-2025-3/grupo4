# config/redis_config.py
import redis
import json
from typing import Any, Optional, Dict, List
from datetime import datetime, timedelta
import os
from pydantic import BaseSettings

class RedisSettings(BaseSettings):
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: Optional[str] = None
    redis_decode_responses: bool = True
    redis_socket_connect_timeout: int = 5
    redis_socket_timeout: int = 5
    
    # Cache TTL settings (in seconds)
    produto_cache_ttl: int = 60*60  # 1 hour
    carrinho_cache_ttl: int = 30*60  # 30 minutes
    session_ttl: int = 24*60*60  # 24 hours
    
    class Config:
        env_file = ".env"

# Singleton Redis connection
class RedisConnection:
    _instance = None
    _redis_client = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RedisConnection, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._redis_client is None:
            settings = RedisSettings()
            self._redis_client = redis.Redis(
                host=settings.redis_host,
                port=settings.redis_port,
                db=settings.redis_db,
                password=settings.redis_password,
                decode_responses=settings.redis_decode_responses,
                socket_connect_timeout=settings.redis_socket_connect_timeout,
                socket_timeout=settings.redis_socket_timeout
            )
    
    @property
    def client(self) -> redis.Redis:
        return self._redis_client
    
    def test_connection(self) -> bool:
        try:
            return self._redis_client.ping()
        except Exception:
            return False

# Redis utility functions
class RedisUtils:
    def __init__(self):
        self.redis_client = RedisConnection().client
        self.settings = RedisSettings()
    
    def serialize_data(self, data: Any) -> str:
        """Serialize data to JSON string for Redis storage."""
        if hasattr(data, 'dict'):  # Pydantic model
            return json.dumps(data.dict(), default=str)
        elif isinstance(data, dict):
            return json.dumps(data, default=str)
        elif isinstance(data, (list, tuple)):
            return json.dumps([item.dict() if hasattr(item, 'dict') else item for item in data], default=str)
        else:
            return json.dumps(data, default=str)
    
    def deserialize_data(self, data: str) -> Any:
        """Deserialize JSON string from Redis."""
        try:
            return json.loads(data)
        except (json.JSONDecodeError, TypeError):
            return data
    
    def set_with_ttl(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set key-value pair with optional TTL."""
        try:
            serialized_value = self.serialize_data(value)
            if ttl:
                return self.redis_client.setex(key, ttl, serialized_value)
            else:
                return self.redis_client.set(key, serialized_value)
        except Exception as e:
            print(f"Redis set error: {e}")
            return False
    
    def get_and_deserialize(self, key: str) -> Optional[Any]:
        """Get value from Redis and deserialize."""
        try:
            value = self.redis_client.get(key)
            if value:
                return self.deserialize_data(value)
            return None
        except Exception as e:
            print(f"Redis get error: {e}")
            return None
    
    def delete_pattern(self, pattern: str) -> int:
        """Delete all keys matching a pattern."""
        try:
            keys = self.redis_client.keys(pattern)
            if keys:
                return self.redis_client.delete(*keys)
            return 0
        except Exception as e:
            print(f"Redis delete pattern error: {e}")
            return 0

# Cache decorator
def cache_result(key_prefix: str, ttl: Optional[int] = None):
    """Decorator to cache function results in Redis."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            redis_utils = RedisUtils()
            
            # Generate cache key
            cache_key = f"{key_prefix}:{hash(str(args) + str(sorted(kwargs.items())))}"
            
            # Try to get from cache
            cached_result = redis_utils.get_and_deserialize(cache_key)
            if cached_result is not None:
                return cached_result
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            if result is not None:
                redis_utils.set_with_ttl(cache_key, result, ttl)
            
            return result
        return wrapper
    return decorator