# services/analytics/app/core/decorators.py
from functools import wraps
from datetime import timedelta
from typing import Optional, Callable

from services.analytics.app.core.cache import AnalyticsCache


cache = AnalyticsCache()

def cached(
    prefix: str,
    ttl: Optional[timedelta] = None,
    cache_null: bool = False
):
    """
    Decorador para cachear resultados de funciones
    
    Args:
        prefix: Prefijo para la clave de caché
        ttl: Tiempo de vida del caché
        cache_null: Si se deben cachear resultados nulos
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Construir clave de caché
            cache_key = await cache.build_key(
                prefix,
                *args,
                *[f"{k}:{v}" for k, v in sorted(kwargs.items())]
            )
            
            # Intentar obtener del caché
            cached_value = await cache.get(cache_key)
            if cached_value is not None:
                return cached_value
            
            # Ejecutar función
            result = await func(*args, **kwargs)
            
            # Guardar en caché si el resultado no es nulo o cache_null es True
            if result is not None or cache_null:
                await cache.set(cache_key, result, ttl)
            
            return result
        return wrapper
    return decorator