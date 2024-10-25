from fastapi import APIRouter
from services.messages.app.api.endpoints import router as messages_router

api_router = APIRouter()
api_router.include_router(messages_router, tags=["messages"])