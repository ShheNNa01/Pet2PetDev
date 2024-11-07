# services/analytics/app/core/decorators.py
from functools import wraps
from datetime import timedelta
import logging
from .cache import cache
from typing import Optional, Any, Callable

logger = logging.getLogger(__name__)

def cached(prefix: str, ttl: Optional[timedelta] = None):
    """
    Decorador para cachear resultados de funciones.
    Si Redis no está disponible, ejecuta la función sin caché.
    
    Args:
        prefix (str): Prefijo para la clave de caché
        ttl (timedelta, optional): Tiempo de vida del caché
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any):
            if not cache.is_available:
                return await func(*args, **kwargs)
                
            try:
                # Construir clave de caché
                cache_key = await cache.build_key(prefix, *args, **kwargs)
                
                # Intentar obtener del caché
                cached_value = await cache.get(cache_key)
                if cached_value is not None:
                    logger.debug(f"Cache hit for key: {cache_key}")
                    return cached_value
                
                # Si no está en caché, ejecutar función
                result = await func(*args, **kwargs)
                
                # Guardar en caché
                await cache.set(cache_key, result, ttl)
                logger.debug(f"Cached result for key: {cache_key}")
                
                return result
            except Exception as e:
                logger.warning(f"Cache error, executing without cache: {str(e)}")
                return await func(*args, **kwargs)
        
        return wrapper
    return decorator