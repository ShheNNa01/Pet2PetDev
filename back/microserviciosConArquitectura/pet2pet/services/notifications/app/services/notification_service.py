from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from typing import List, Optional

from shared.database.models import Notification, User, Pet, Post
from services.notifications.app.models.schemas import (
    NotificationCreate,
    NotificationResponse,
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
                    detail="User not found"
                )

            # Crear la notificación
            db_notification = Notification(
                user_id=notification_data.user_id,
                type=notification_data.type,
                related_id=notification_data.related_id,
                message=notification_data.message,
                is_read=False
            )

            db.add(db_notification)
            db.commit()
            db.refresh(db_notification)

            return db_notification

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
        """Obtener notificaciones de un usuario"""
        query = db.query(Notification).filter(Notification.user_id == user_id)

        if notification_type:
            query = query.filter(Notification.type == notification_type)
        
        if is_read is not None:
            query = query.filter(Notification.is_read == is_read)

        return query.order_by(Notification.created_at.desc()).offset(skip).limit(limit).all()

    @staticmethod
    async def mark_as_read(
        db: Session,
        notification_id: int,
        user_id: int
    ) -> Notification:
        """Marcar una notificación como leída"""
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
        db.commit()
        db.refresh(notification)

        return notification

    @staticmethod
    async def mark_all_as_read(
        db: Session,
        user_id: int
    ) -> None:
        """Marcar todas las notificaciones de un usuario como leídas"""
        db.query(Notification).filter(
            Notification.user_id == user_id,
            Notification.is_read == False
        ).update({"is_read": True})
        
        db.commit()

    @staticmethod
    async def get_notification_count(
        db: Session,
        user_id: int
    ) -> dict:
        """Obtener conteo de notificaciones"""
        total = db.query(func.count(Notification.notification_id)).filter(
            Notification.user_id == user_id
        ).scalar()

        unread = db.query(func.count(Notification.notification_id)).filter(
            Notification.user_id == user_id,
            Notification.is_read == False
        ).scalar()

        return {
            "total": total,
            "unread": unread
        }

    @staticmethod
    async def delete_notification(
        db: Session,
        notification_id: int,
        user_id: int
    ) -> None:
        """Eliminar una notificación"""
        notification = db.query(Notification).filter(
            Notification.notification_id == notification_id,
            Notification.user_id == user_id
        ).first()

        if not notification:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Notification not found"
            )

        db.delete(notification)
        db.commit()

    @staticmethod
    async def create_notification_for_event(
        db: Session,
        event_type: NotificationType,
        user_id: int,
        related_id: Optional[int] = None,
        custom_message: Optional[str] = None,
        additional_data: Optional[dict] = None
    ) -> Notification:
        """Helper method to create notifications for different events with context"""
        
        # Mensajes predeterminados según el tipo de evento
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
            # Crear la notificación
            notification_data = NotificationCreate(
                user_id=user_id,
                type=event_type,
                related_id=related_id,
                message=custom_message or default_messages.get(event_type, "Nueva notificación")
            )

            db_notification = Notification(
                **notification_data.dict(),
                is_read=False
            )

            # Si hay datos adicionales, los guardamos como JSON
            if additional_data:
                db_notification.additional_data = additional_data

            db.add(db_notification)
            db.commit()
            db.refresh(db_notification)

            return db_notification
        except Exception as e:
            db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating notification: {str(e)}"
        )
    @staticmethod
    async def get_notifications_with_context(
        db: Session,
        user_id: int,
        skip: int = 0,
        limit: int = 50,
        notification_type: Optional[NotificationType] = None,
        is_read: Optional[bool] = None
    ) -> List[NotificationResponse]:
        """Get notifications with additional context information"""
        try:
            query = db.query(Notification).filter(Notification.user_id == user_id)

            if notification_type:
                query = query.filter(Notification.type == notification_type)
            
            if is_read is not None:
                query = query.filter(Notification.is_read == is_read)

            notifications = query.order_by(Notification.created_at.desc())\
                            .offset(skip)\
                            .limit(limit)\
                            .all()

            # Enriquecer notificaciones con contexto
            result = []
            for notif in notifications:
                response = NotificationResponse.from_orm(notif)
                
                # Añadir información contextual según el tipo
                if notif.related_id:
                    if notif.type == NotificationType.NEW_FOLLOWER:
                        pet = db.query(Pet).filter(Pet.pet_id == notif.related_id).first()
                        if pet:
                            response.related_pet_name = pet.name

                    elif notif.type in [NotificationType.NEW_COMMENT, NotificationType.NEW_REACTION]:
                        post = db.query(Post).filter(Post.post_id == notif.related_id).first()
                        if post:
                            response.related_post_preview = post.content[:100] + "..."

                result.append(response)

            return result

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error getting notifications: {str(e)}"
            )