from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List, Optional, Union
from pydantic import EmailStr, validator
import json

class Settings(BaseSettings):
    # Configuración básica de la aplicación
    APP_NAME: str = "Pet2Pet"
    DEBUG: bool = False
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api/v1"
    
    # Database
    DATABASE_URL: str
    
    # Security
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"
    
    # CORS
    CORS_ORIGINS: Union[str, List[str]] = ["http://localhost:3000", "http://localhost:5173"]
    
    # Service Discovery
    SERVICE_DISCOVERY_HOST: str = "localhost"
    SERVICE_DISCOVERY_PORT: int = 8500
    
    # Puertos de servicios
    AUTH_SERVICE_PORT: int = 8000
    POSTS_SERVICE_PORT: int = 8001
    MESSAGES_SERVICE_PORT: int = 8002
    NOTIFICATIONS_SERVICE_PORT: int = 8003
    PETS_SERVICE_PORT: int = 8004
    GROUPS_SERVICE_PORT: int = 8005

    # Configuración de archivos
    MAX_FILE_SIZE: int = 5_242_880  # 5MB en bytes
    ALLOWED_FILE_TYPES: List[str] = ["image/jpeg", "image/png", "image/jpg"]
    UPLOAD_FOLDER: str = "uploads"

    # Configuración de paginación
    DEFAULT_PAGE_SIZE: int = 10
    MAX_PAGE_SIZE: int = 100

    # Redis y Cache (opcional)
    REDIS_ENABLED: bool = False
    REDIS_URL: Optional[str] = None
    REDIS_MAX_CONNECTIONS: int = 10
    REDIS_TIMEOUT: int = 30
    CACHE_ENABLED: bool = False
    CACHE_TTL: int = 3600

    # Notifications
    NOTIFICATION_WORKER_ENABLED: bool = False
    NOTIFICATION_BATCH_SIZE: int = 100
    NOTIFICATION_PROCESSING_INTERVAL: float = 0.1

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    ENABLE_FILE_LOGGING: bool = True
    LOG_FILE_PATH: str = "logs/pet2pet.log"

    # Rate Limiting
    ENABLE_RATE_LIMIT: bool = False
    RATE_LIMIT_PER_MINUTE: int = 100

    # Storage
    STORAGE_TYPE: str = "local"  # "local" o "s3"
    S3_BUCKET_NAME: Optional[str] = None
    S3_ACCESS_KEY: Optional[str] = None
    S3_SECRET_KEY: Optional[str] = None
    S3_REGION: Optional[str] = None

    class Config:
        env_file = ".env"
        case_sensitive = True

    @validator('CORS_ORIGINS', pre=True)
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return [origin.strip() for origin in v.split(",")]
        return v

    def get_database_connection_args(self):
        return {
            "min_size": 5,
            "max_size": 20,
            "force_rollback": self.DEBUG
        }
    
    def get_redis_connection_args(self):
        if not self.REDIS_ENABLED:
            return None
        return {
            "max_connections": self.REDIS_MAX_CONNECTIONS,
            "timeout": self.REDIS_TIMEOUT,
        }

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()