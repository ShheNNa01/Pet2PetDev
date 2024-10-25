from fastapi import APIRouter
from services.notifications.app.api.endpoints import router as notifications_router

api_router = APIRouter()
api_router.include_router(notifications_router, tags=["notifications"])