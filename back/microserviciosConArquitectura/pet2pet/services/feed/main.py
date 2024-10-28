from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from shared.config.settings import settings
from app.api.routes import api_router

# Configurar logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format=settings.LOG_FORMAT,
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(settings.LOG_FILE_PATH) if settings.ENABLE_FILE_LOGGING else logging.NullHandler()
    ]
)

app = FastAPI(
    title="Feed Service",
    description="Service for managing user feeds in Pet2Pet",
    version=settings.VERSION,
    docs_url=f"{settings.API_PREFIX}/feed/docs",
    redoc_url=f"{settings.API_PREFIX}/feed/redoc",
    openapi_url=f"{settings.API_PREFIX}/feed/openapi.json"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas
app.include_router(api_router, prefix=settings.API_PREFIX)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.FEED_SERVICE_PORT,
        reload=settings.DEBUG
    )