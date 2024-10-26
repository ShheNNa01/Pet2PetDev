from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from shared.config.settings import settings
import uvicorn
import logging
from app.api.routes import api_router

# Configurar logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format=settings.LOG_FORMAT,
    filename=settings.LOG_FILE_PATH if settings.ENABLE_FILE_LOGGING else None
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Groups Service",
    description="Service for managing groups in Pet2Pet",
    version=settings.VERSION,
    docs_url="/api/v1/groups/docs",
    redoc_url="/api/v1/groups/redoc",
    openapi_url="/api/v1/groups/openapi.json"
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

@app.on_event("startup")
async def startup_event():
    logger.info("Starting Groups Service...")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down Groups Service...")

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "groups",
        "version": settings.VERSION
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.GROUPS_SERVICE_PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )