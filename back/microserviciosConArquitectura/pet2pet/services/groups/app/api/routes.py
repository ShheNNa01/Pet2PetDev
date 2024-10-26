from fastapi import APIRouter
from services.groups.app.api.endpoints import router as groups_router

api_router = APIRouter()
api_router.include_router(groups_router, tags=["groups"])