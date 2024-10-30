# services/analytics/app/core/cache.py
from redis import Redis
from json import dumps, loads
from typing import Any, Optional
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)

class AnalyticsCache:
    def __init__(self, redis_url: str = "redis://localhost:6379/0"):
        self.redis = Redis.from_url(redis_url, decode_responses=True)
        self.default_ttl = timedelta(minutes=15)  # Cache por defecto 15 minutos

    async def get(self, key: str) -> Optional[Any]:
        """Obtiene un valor del caché"""
        try:
            data = self.redis.get(key)
            if data:
                return loads(data)
            return None
        except Exception as e:
            logger.error(f"Error getting cache for key {key}: {str(e)}")
            return None

    async def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[timedelta] = None
    ) -> bool:
        """Guarda un valor en el caché"""
        try:
            ttl_seconds = int(ttl.total_seconds()) if ttl else int(self.default_ttl.total_seconds())
            return self.redis.setex(
                name=key,
                time=ttl_seconds,
                value=dumps(value)
            )
        except Exception as e:
            logger.error(f"Error setting cache for key {key}: {str(e)}")
            return False

    async def delete(self, key: str) -> bool:
        """Elimina un valor del caché"""
        try:
            return bool(self.redis.delete(key))
        except Exception as e:
            logger.error(f"Error deleting cache for key {key}: {str(e)}")
            return False

    async def build_key(self, *args: Any) -> str:
        """Construye una clave de caché a partir de los argumentos"""
        return ":".join(str(arg) for arg in args)