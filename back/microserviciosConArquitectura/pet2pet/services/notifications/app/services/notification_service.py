from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime
from typing import List, Optional, Dict

from shared.database.models import Notification, User
from services.notifications.app.models.schemas import (
    NotificationCreate,
    NotificationType,
    NotificationUpdate
)

class NotificationService:
    @staticmethod
    async def create_notification(
        db: Session,
        notification_data: NotificationCreate
    ) -> Notification:
        """Crear una nueva notificación"""
        try:
            # Verificar que el usuario existe
            user = db.query(User).filter(User.user_id == notification_data.user_id).first()
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"User {notification_data.user_id} not found"
                )

            # Crear la notificación
            db_notification = Notification(
                user_id=notification_data.user_id,
                type=notification_data.type,
                related_id=notification_data.related_id,
                message=notification_data.message,
                additional_data=notification_data.additional_data,
                is_read=False,
                created_at=datetime.utcnow()
            )

            db.add(db_notification)
            db.commit()
            db.refresh(db_notification)

            return db_notification

        except HTTPException:
            db.rollback()
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating notification: {str(e)}"
            )

    @staticmethod
    async def get_notifications(
        db: Session,
        user_id: int,
        skip: int = 0,
        limit: int = 50,
        notification_type: Optional[NotificationType] = None,
        is_read: Optional[bool] = None
    ) -> List[Notification]:
        """Obtener notificaciones de un usuario con filtros"""
        try:
            query = db.query(Notification).filter(Notification.user_id == user_id)

            if notification_type:
                query = query.filter(Notification.type == notification_type)
            
            if is_read is not None:
                query = query.filter(Notification.is_read == is_read)

            return query.order_by(desc(Notification.created_at)).offset(skip).limit(limit).all()

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error retrieving notifications: {str(e)}"
            )

    @staticmethod
    async def mark_as_read(
        db: Session,
        notification_id: int,
        user_id: int
    ) -> Notification:
        """Marcar una notificación como leída"""
        try:
            notification = db.query(Notification).filter(
                Notification.notification_id == notification_id,
                Notification.user_id == user_id
            ).first()

            if not notification:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Notification not found"
                )

            notification.is_read = True
            notification.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(notification)

            return notification

        except HTTPException:
            db.rollback()
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error marking notification as read: {str(e)}"
            )

    @staticmethod
    async def mark_all_as_read(
        db: Session,
        user_id: int
    ) -> None:
        """Marcar todas las notificaciones de un usuario como leídas"""
        try:
            db.query(Notification).filter(
                Notification.user_id == user_id,
                Notification.is_read == False
            ).update({
                "is_read": True,
                "updated_at": datetime.utcnow()
            })
            
            db.commit()

        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error marking notifications as read: {str(e)}"
            )

    @staticmethod
    async def get_notification_count(
        db: Session,
        user_id: int
    ) -> Dict:
        """Obtener conteo de notificaciones"""
        try:
            total = db.query(func.count(Notification.notification_id))\
                     .filter(Notification.user_id == user_id)\
                     .scalar()

            unread = db.query(func.count(Notification.notification_id))\
                      .filter(
                          Notification.user_id == user_id,
                          Notification.is_read == False
                      ).scalar()

            # Conteo por tipo
            type_counts = db.query(
                Notification.type,
                func.count(Notification.notification_id)
            ).filter(
                Notification.user_id == user_id
            ).group_by(
                Notification.type
            ).all()

            by_type = {str(t): c for t, c in type_counts}

            return {
                "total": total,
                "unread": unread,
                "by_type": by_type
            }

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error getting notification count: {str(e)}"
            )

    @staticmethod
    async def create_notification_for_event(
        db: Session,
        event_type: NotificationType,
        user_id: int,
        related_id: Optional[int] = None,
        custom_message: Optional[str] = None,
        additional_data: Optional[dict] = None
    ) -> Notification:
        """Helper method para crear notificaciones para diferentes eventos"""
        
        default_messages = {
            NotificationType.NEW_MESSAGE: "Has recibido un nuevo mensaje",
            NotificationType.NEW_COMMENT: "Alguien ha comentado en tu publicación",
            NotificationType.NEW_REACTION: "A alguien le ha gustado tu publicación",
            NotificationType.NEW_FOLLOWER: "Tienes un nuevo seguidor",
            NotificationType.MENTION: "Te han mencionado en una publicación",
            NotificationType.POST_SHARED: "Han compartido tu publicación",
            NotificationType.POST_FROM_FOLLOWING: "Una mascota que sigues ha publicado algo nuevo",
            NotificationType.COMMENT_REPLY: "Alguien ha respondido a tu comentario",
            NotificationType.SYSTEM: "Notificación del sistema"
        }

        try:
            notification_data = NotificationCreate(
                user_id=user_id,
                type=event_type,
                related_id=related_id,
                message=custom_message or default_messages.get(event_type, "Nueva notificación"),
                additional_data=additional_data
            )

            return await NotificationService.create_notification(db, notification_data)

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating event notification: {str(e)}"
            )