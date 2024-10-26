from fastapi import APIRouter
from services.search.app.api.endpoints import router as search_router

api_router = APIRouter()
api_router.include_router(search_router, tags=["search"])