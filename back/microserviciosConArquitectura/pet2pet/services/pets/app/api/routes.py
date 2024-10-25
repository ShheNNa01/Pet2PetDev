from fastapi import APIRouter
from services.pets.app.api.endpoints import (
    router as pets_router,
    types_router,
    breeds_router
)

api_router = APIRouter()

# Incluir los routers en orden específico
api_router.include_router(types_router, tags=["pet-types"])
api_router.include_router(breeds_router, tags=["pet-breeds"])
api_router.include_router(pets_router, tags=["pets"])