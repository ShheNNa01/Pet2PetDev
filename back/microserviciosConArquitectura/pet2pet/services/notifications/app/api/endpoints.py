from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from shared.database.session import get_db
from shared.database.models import User, Notification
from services.notifications.app.models.schemas import (
    NotificationResponse,
    NotificationCreate,
    NotificationUpdate,
    NotificationCount,
    NotificationType
)
from services.notifications.app.services.notification_service import NotificationService
from services.auth.app.api.dependencies import get_current_active_user

router = APIRouter()

@router.get("/", response_model=List[NotificationResponse])
async def get_notifications(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    notification_type: Optional[NotificationType] = None,
    is_read: Optional[bool] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Obtener las notificaciones del usuario actual
    """
    return await NotificationService.get_notifications(
        db,
        current_user.user_id,
        skip,
        limit,
        notification_type,
        is_read
    )

@router.get("/count", response_model=NotificationCount)
async def get_notification_count(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Obtener el conteo de notificaciones del usuario actual
    """
    return await NotificationService.get_notification_count(db, current_user.user_id)

@router.post("/{notification_id}/read", response_model=NotificationResponse)
async def mark_notification_as_read(
    notification_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Marcar una notificación específica como leída
    """
    return await NotificationService.mark_as_read(db, notification_id, current_user.user_id)

@router.post("/read-all", status_code=status.HTTP_200_OK)
async def mark_all_notifications_as_read(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Marcar todas las notificaciones como leídas
    """
    await NotificationService.mark_all_as_read(db, current_user.user_id)
    return {"message": "All notifications marked as read"}

@router.delete("/{notification_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_notification(
    notification_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Eliminar una notificación específica
    """
    await NotificationService.delete_notification(db, notification_id, current_user.user_id)
    return {"message": "Notification deleted"}

# Endpoints para crear notificaciones desde otros servicios
@router.post("/internal/create", response_model=NotificationResponse, include_in_schema=False)
async def create_notification(
    notification: NotificationCreate,
    db: Session = Depends(get_db)
):
    """
    Endpoint interno para crear notificaciones desde otros servicios
    """
    return await NotificationService.create_notification(db, notification)