from fastapi import APIRouter
from services.auth.app.api.endpoints import router as auth_router

api_router = APIRouter()
api_router.include_router(auth_router, prefix="/auth")  # Añadimos el prefijo