# services/auth/api/routes.py
from fastapi import APIRouter
from services.auth.api.endpoints import router as auth_router

api_router = APIRouter()
api_router.include_router(auth_router, prefix="/auth", tags=["authentication"])