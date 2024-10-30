# services/virtual_pet/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import api_router
from app.core.docs import tags_metadata
from shared.config.settings import settings

description = """
# 🐾 Pet2Pet Virtual Pet API

Esta API permite gestionar mascotas virtuales dentro de la plataforma Pet2Pet.
Las mascotas virtuales son compañeros digitales que evolucionan basándose en las 
interacciones del usuario en la red social.

## Características Principales

* **Mascotas Virtuales**: Crear y gestionar mascotas virtuales
* **Sistema de Niveles**: Las mascotas suben de nivel al ganar experiencia
* **Acciones**: Realizar diferentes actividades como alimentar, jugar y socializar
* **Logros**: Desbloquear logros especiales y recibir recompensas
* **Estadísticas**: Seguimiento detallado del progreso y estado de la mascota

## Notas de Uso

* Las estadísticas de la mascota se actualizan en tiempo real
* Los atributos disminuyen con el tiempo si no hay interacción
* Cada nivel requiere más experiencia que el anterior
* Los logros otorgan bonificaciones especiales
"""

app = FastAPI(
    title="Pet2Pet Virtual Pet Service",
    description=description,
    version="1.0.0",
    openapi_url=f"{settings.API_PREFIX}/openapi.json",
    docs_url=f"{settings.API_PREFIX}/docs",
    openapi_tags=tags_metadata,
    redoc_url=f"{settings.API_PREFIX}/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"]
)

app.include_router(api_router, prefix=settings.API_PREFIX)

@app.get("/", tags=["status"])
async def root():
    """
    Endpoint de verificación de estado del servicio.
    """
    return {
        "service": "Pet2Pet Virtual Pet Service",
        "status": "online",
        "version": "1.0.0"
    }