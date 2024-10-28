from fastapi import APIRouter
from services.moderation.app.api.endpoints import router as moderation_router

api_router = APIRouter()
api_router.include_router(moderation_router, tags=["moderation"])