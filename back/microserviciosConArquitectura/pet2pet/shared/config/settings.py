# shared/config/settings.py
from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List, Optional

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
    
    # Service Discovery - Añadido para resolver el error
    SERVICE_DISCOVERY_HOST: str = "localhost"
    SERVICE_DISCOVERY_PORT: int = 8500
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173"
    ]
    
    # Puertos de servicios
    AUTH_SERVICE_PORT: int = 8000
    POSTS_SERVICE_PORT: int = 8001
    MESSAGES_SERVICE_PORT: int = 8002
    NOTIFICATIONS_SERVICE_PORT: int = 8003
    PETS_SERVICE_PORT: int = 8004

    # Configuración de archivos
    MAX_FILE_SIZE: int = 5_242_880  # 5MB
    ALLOWED_FILE_TYPES: List[str] = ["image/jpeg", "image/png", "image/jpg"]
    UPLOAD_FOLDER: str = "uploads"

    # Configuración de paginación
    DEFAULT_PAGE_SIZE: int = 10
    MAX_PAGE_SIZE: int = 100

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 100

    # Logging
    LOG_LEVEL: str = "INFO"
    ENABLE_FILE_LOGGING: bool = True
    LOG_FILE_PATH: str = "logs/pet2pet.log"

    class Config:
        env_file = ".env"
        case_sensitive = True

    def get_database_connection_args(self):
        return {
            "min_size": 5,
            "max_size": 20,
            "force_rollback": self.DEBUG
        }

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()