from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from shared.config.settings import settings
from shared.database.models import Notification, User, Pet, Post
from services.notifications.app.models.schemas import (
    NotificationCreate,
    NotificationResponse,
    NotificationType,
    NotificationUpdate
)

# Solo importar event_broker si Redis está habilitado
event_broker = None
if settings.REDIS_ENABLED:
    from services.notifications.app.core.event_broker import event_broker

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
                is_read=False,
                created_at=datetime.utcnow()
            )

            db.add(db_notification)
            db.commit()
            db.refresh(db_notification)

            # Si Redis está habilitado, publicar el evento
            if settings.REDIS_ENABLED and event_broker:
                try:
                    await event_broker.publish_event(
                        "notifications",
                        {
                            "type": "new_notification",
                            "notification_id": db_notification.notification_id,
                            "user_id": db_notification.user_id,
                            "notification_type": notification_data.type,
                            "message": notification_data.message
                        }
                    )
                except Exception as redis_error:
                    # Log el error pero no fallar la creación de la notificación
                    print(f"Error publishing to Redis: {str(redis_error)}")

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
        is_read: Optional[bool] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Notification]:
        """Obtener notificaciones de un usuario con filtros"""
        try:
            query = db.query(Notification).filter(Notification.user_id == user_id)

            # Aplicar filtros
            if notification_type:
                query = query.filter(Notification.type == notification_type)
            
            if is_read is not None:
                query = query.filter(Notification.is_read == is_read)

            if start_date:
                query = query.filter(Notification.created_at >= start_date)

            if end_date:
                query = query.filter(Notification.created_at <= end_date)

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
        user_id: int,
        notification_type: Optional[NotificationType] = None
    ) -> Dict[str, int]:
        """Marcar todas las notificaciones de un usuario como leídas"""
        try:
            query = db.query(Notification).filter(
                Notification.user_id == user_id,
                Notification.is_read == False
            )

            if notification_type:
                query = query.filter(Notification.type == notification_type)

            updated_count = query.update({
                "is_read": True,
                "updated_at": datetime.utcnow()
            })
            
            db.commit()
            return {"updated_count": updated_count}

        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error marking notifications as read: {str(e)}"
            )

    @staticmethod
    async def get_notification_count(
        db: Session,
        user_id: int,
        include_types: bool = False
    ) -> Dict[str, Any]:
        """Obtener conteo de notificaciones con estadísticas detalladas"""
        try:
            total = db.query(func.count(Notification.notification_id)).filter(
                Notification.user_id == user_id
            ).scalar()

            unread = db.query(func.count(Notification.notification_id)).filter(
                Notification.user_id == user_id,
                Notification.is_read == False
            ).scalar()

            result = {
                "total": total,
                "unread": unread
            }

            if include_types:
                # Contar notificaciones por tipo
                type_counts = db.query(
                    Notification.type,
                    func.count(Notification.notification_id).label('count')
                ).filter(
                    Notification.user_id == user_id
                ).group_by(
                    Notification.type
                ).all()

                result["by_type"] = {
                    notification_type: count for notification_type, count in type_counts
                }

            return result

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error getting notification count: {str(e)}"
            )

    @staticmethod
    async def delete_notification(
        db: Session,
        notification_id: int,
        user_id: int
    ) -> None:
        """Eliminar una notificación"""
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

            db.delete(notification)
            db.commit()

        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error deleting notification: {str(e)}"
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

    @staticmethod
    async def get_notifications_with_context(
        db: Session,
        user_id: int,
        skip: int = 0,
        limit: int = 50,
        days: Optional[int] = None
    ) -> List[NotificationResponse]:
        """Get notifications with additional context information"""
        try:
            query = db.query(Notification).filter(Notification.user_id == user_id)

            if days:
                cutoff_date = datetime.utcnow() - timedelta(days=days)
                query = query.filter(Notification.created_at >= cutoff_date)

            notifications = query.order_by(desc(Notification.created_at))\
                            .offset(skip)\
                            .limit(limit)\
                            .all()

            # Enriquecer notificaciones con contexto
            result = []
            for notif in notifications:
                notification_response = NotificationResponse.model_validate(notif)
                
                # Añadir información contextual según el tipo
                if notif.related_id:
                    if notif.type == NotificationType.NEW_FOLLOWER:
                        pet = db.query(Pet).filter(Pet.pet_id == notif.related_id).first()
                        if pet:
                            notification_response.context = {
                                "pet_name": pet.name,
                                "pet_picture": pet.pet_picture
                            }

                    elif notif.type in [NotificationType.NEW_COMMENT, NotificationType.NEW_REACTION]:
                        post = db.query(Post).filter(Post.post_id == notif.related_id).first()
                        if post:
                            notification_response.context = {
                                "post_preview": post.content[:100] + "..." if len(post.content) > 100 else post.content,
                                "post_id": post.post_id
                            }

                result.append(notification_response)

            return result

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error getting notifications with context: {str(e)}"
            )