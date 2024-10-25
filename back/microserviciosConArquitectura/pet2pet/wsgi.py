# wsgi.py
from pathlib import Path
import sys
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Añadir el directorio raíz al PYTHONPATH
ROOT_PATH = Path(__file__).resolve().parent
sys.path.append(str(ROOT_PATH))

from shared.config.settings import settings

# Crear la aplicación principal
app = FastAPI(
    title="Pet2Pet API",
    description="Pet2Pet Platform API Gateway",
    version="1.0.0",
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Importar las rutas de los servicios
from services.auth.app.api.routes import api_router as auth_router
from services.pets.app.api.routes import api_router as pets_router
from services.posts.app.api.routes import api_router as posts_router
from services.messages.app.api.routes import api_router as message_router
from services.notifications.app.api.routes import api_router as notifications_router

# Incluir las rutas
app.include_router(auth_router, prefix="/api/v1")
app.include_router(pets_router, prefix="/api/v1")
app.include_router(posts_router, prefix="/api/v1")
app.include_router(message_router, prefix="/api/v1")
app.include_router(notifications_router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run("wsgi:app", host="0.0.0.0", port=8000, reload=True)