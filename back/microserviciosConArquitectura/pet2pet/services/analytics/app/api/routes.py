# services/analytics/app/api/routes.py
from fastapi import APIRouter
from services.analytics.app.api.endpoints import router as analytics_router

api_router = APIRouter()
api_router.include_router(analytics_router, tags=["analytics"])