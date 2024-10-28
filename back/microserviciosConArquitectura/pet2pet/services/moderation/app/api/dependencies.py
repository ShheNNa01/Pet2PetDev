# services/moderation/app/api/dependencies.py
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from shared.database.session import get_db
from shared.database.models import User
from services.moderation.app.services.moderation_service import ModerationService
from services.moderation.app.services.queue_service import QueueService
from services.moderation.app.services.report_service import ReportService
from services.moderation.app.services.content_filter_service import ContentFilterService

# Servicios singleton
_content_filter_service = None
_moderation_service = None
_queue_service = None
_report_service = None

def get_content_filter_service() -> ContentFilterService:
    global _content_filter_service
    if _content_filter_service is None:
        _content_filter_service = ContentFilterService()
    return _content_filter_service

def get_moderation_service() -> ModerationService:
    """
    Retorna una instancia singleton del servicio de moderación
    """
    global _moderation_service
    if _moderation_service is None:
        _moderation_service = ModerationService()
    return _moderation_service

def get_queue_service() -> QueueService:
    """
    Retorna una instancia singleton del servicio de cola
    """
    global _queue_service
    if _queue_service is None:
        _queue_service = QueueService()
    return _queue_service

def get_report_service() -> ReportService:
    """
    Retorna una instancia singleton del servicio de reportes
    """
    global _report_service
    if _report_service is None:
        _report_service = ReportService()
    return _report_service

async def get_current_user(
    db: Session = Depends(get_db),
    # Aquí deberías incluir la lógica de autenticación
) -> User:
    """
    Obtiene el usuario actual autenticado
    """
    # Implementar lógica de autenticación
    pass

async def get_current_moderator(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Verifica que el usuario actual tenga permisos de moderador
    """
    if not current_user.role or current_user.role.role_name not in ["moderator", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges"
        )
    return current_user