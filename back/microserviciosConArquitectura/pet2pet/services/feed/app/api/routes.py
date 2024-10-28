from fastapi import APIRouter
from services.feed.app.api.endpoints import router as feed_router

api_router = APIRouter()
api_router.include_router(feed_router, tags=["feed"])