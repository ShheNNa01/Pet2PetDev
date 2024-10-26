from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from shared.config.settings import settings
import logging
import os
import sys
from pathlib import Path

def setup_logging():
    """Configura el sistema de logging"""
    log_directory = os.path.dirname(settings.LOG_FILE_PATH)
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
        
    logging.basicConfig(
        level=settings.LOG_LEVEL,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(settings.LOG_FILE_PATH) if settings.ENABLE_FILE_LOGGING else logging.NullHandler()
        ]
    )

def create_app() -> FastAPI:
    """Crea y configura la aplicación FastAPI"""
    
    # Configurar logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # Imprimir PYTHONPATH actual
    logger.info(f"PYTHONPATH: {sys.path}")
    
    app = FastAPI(
        title=settings.APP_NAME,
        description="Pet2Pet Platform API Gateway",
        version=settings.VERSION,
        docs_url=f"{settings.API_PREFIX}/docs",
        redoc_url=f"{settings.API_PREFIX}/redoc",
        openapi_url=f"{settings.API_PREFIX}/openapi.json"
    )

    # Configurar CORS
    if isinstance(settings.CORS_ORIGINS, str):
        origins = [settings.CORS_ORIGINS]
    else:
        origins = settings.CORS_ORIGINS
        
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Health check endpoint
    @app.get("/health")
    async def health_check():
        return {"status": "healthy", "version": settings.VERSION}

    # Importar las rutas de los servicios
    services_config = [
        {
            'name': 'auth',
            'module': 'services.auth.app.api.routes',
            'prefix': '/auth'
        },
        {
            'name': 'pets',
            'module': 'services.pets.app.api.routes',
            'prefix': '/pets'
        },
        {
            'name': 'posts',
            'module': 'services.posts.app.api.routes',
            'prefix': '/posts'
        },
        {
            'name': 'messages',
            'module': 'services.messages.app.api.routes',
            'prefix': '/messages'
        },
        {
            'name': 'notifications',
            'module': 'services.notifications.app.api.routes',
            'prefix': '/notifications'
        },
        {
            'name': 'groups',
            'module': 'services.groups.app.api.routes',
            'prefix': '/groups'
        },
        {
            'name': 'search',
            'module': 'services.search.app.api.routes',
            'prefix': '/search'
        }
    ]

    for service in services_config:
        try:
            logger.info(f"Loading routes for {service['name']} service from {service['module']}")
            module = __import__(service['module'], fromlist=['api_router'])
            router = getattr(module, 'api_router')
            app.include_router(
                router,
                prefix=f"{settings.API_PREFIX}{service['prefix']}",
                tags=[service['name']]
            )
            logger.info(f"Successfully loaded routes for {service['name']} service")
        except Exception as e:
            logger.error(f"Error loading {service['name']} service: {str(e)}")
            logger.exception(e)

    @app.on_event("startup")
    async def startup_event():
        logger.info("Starting Pet2Pet API Gateway...")
        # Log all registered routes
        for route in app.routes:
            logger.info(f"Registered route: {route.path}")

    @app.on_event("shutdown")
    async def shutdown_event():
        logger.info("Shutting down Pet2Pet API Gateway...")

    return app