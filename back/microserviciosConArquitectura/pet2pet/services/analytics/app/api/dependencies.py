# services/analytics/app/api/dependencies.py
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from shared.database.session import get_db
from shared.database.models import User

from services.analytics.app.services.user_analytics import UserAnalyticsService
from services.analytics.app.services.content_analytics import ContentAnalyticsService
from services.analytics.app.services.engagement_analytics import EngagementAnalyticsService
from services.analytics.app.services.platform_analytics import PlatformAnalyticsService

# Servicios singleton
_user_analytics = None
_content_analytics = None
_engagement_analytics = None
_platform_analytics = None

def get_user_analytics_service() -> UserAnalyticsService:
    global _user_analytics
    if _user_analytics is None:
        _user_analytics = UserAnalyticsService()
    return _user_analytics

def get_content_analytics_service() -> ContentAnalyticsService:
    global _content_analytics
    if _content_analytics is None:
        _content_analytics = ContentAnalyticsService()
    return _content_analytics

def get_engagement_analytics_service() -> EngagementAnalyticsService:
    global _engagement_analytics
    if _engagement_analytics is None:
        _engagement_analytics = EngagementAnalyticsService()
    return _engagement_analytics

def get_platform_analytics_service() -> PlatformAnalyticsService:
    global _platform_analytics
    if _platform_analytics is None:
        _platform_analytics = PlatformAnalyticsService()
    return _platform_analytics

async def get_current_admin(
    db: Session = Depends(get_db),
    # Implementar lógica de autenticación
) -> User:
    """
    Verifica que el usuario actual sea un administrador.
    """
    # Implementar verificación de permisos
    pass