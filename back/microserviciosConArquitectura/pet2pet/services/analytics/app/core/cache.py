# services/analytics/app/core/cache.py
from redis import Redis, ConnectionError, RedisError
from json import dumps, loads
from typing import Any, Optional
from datetime import timedelta
import logging
from functools import wraps

logger = logging.getLogger(__name__)

class AnalyticsCache:
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, redis_url: str = "redis://localhost:6379/0"):
        if not hasattr(self, 'initialized'):
            self.redis = None
            self.is_available = False
            self.default_ttl = timedelta(minutes=15)
            self.initialized = True
            self._initialize_redis(redis_url)
    
    def _initialize_redis(self, redis_url: str):
        """Inicializa la conexión a Redis"""
        try:
            self.redis = Redis.from_url(redis_url, decode_responses=True)
            self.redis.ping()
            self.is_available = True
            logger.info("Redis cache initialized successfully")
        except (ConnectionError, RedisError) as e:
            self.is_available = False
            logger.warning(f"Redis cache unavailable, running without cache: {str(e)}")

    async def get(self, key: str) -> Optional[Any]:
        """Obtiene un valor del caché"""
        if not self.is_available:
            return None
            
        try:
            data = self.redis.get(key)
            if data:
                return loads(data)
            return None
        except Exception as e:
            logger.warning(f"Error getting cache for key {key}: {str(e)}")
            return None

    async def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[timedelta] = None
    ) -> bool:
        """Guarda un valor en el caché"""
        if not self.is_available:
            return False
            
        try:
            ttl_seconds = int(ttl.total_seconds()) if ttl else int(self.default_ttl.total_seconds())
            return self.redis.setex(
                name=key,
                time=ttl_seconds,
                value=dumps(value)
            )
        except Exception as e:
            logger.warning(f"Error setting cache for key {key}: {str(e)}")
            return False

    async def delete(self, key: str) -> bool:
        """Elimina un valor del caché"""
        if not self.is_available:
            return False
            
        try:
            return bool(self.redis.delete(key))
        except Exception as e:
            logger.warning(f"Error deleting cache for key {key}: {str(e)}")
            return False

    async def build_key(self, *args: Any) -> str:
        """Construye una clave de caché a partir de los argumentos"""
        return ":".join(str(arg) for arg in args)
        
    def check_health(self) -> bool:
        """Verifica si Redis está disponible"""
        if not self.is_available:
            return False
            
        try:
            self.redis.ping()
            return True
        except:
            self.is_available = False
            return False

cache = AnalyticsCache()