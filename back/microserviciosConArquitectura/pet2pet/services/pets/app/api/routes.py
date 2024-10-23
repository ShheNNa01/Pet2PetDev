from fastapi import APIRouter
from services.pets.app.api.endpoints import router as pets_router

api_router = APIRouter()
api_router.include_router(pets_router, prefix="/pets")  # Añadimos el prefijo