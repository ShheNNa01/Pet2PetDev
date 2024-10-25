from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum

class NotificationType(str, Enum):
    NEW_MESSAGE = "new_message"          # Para mensajes privados
    NEW_COMMENT = "new_comment"          # Para comentarios en posts
    NEW_REACTION = "new_reaction"        # Para reacciones en posts
    NEW_FOLLOWER = "new_follower"        # Para nuevos seguidores
    MENTION = "mention"                  # Para menciones en posts o comentarios
    POST_SHARED = "post_shared"          # Para cuando comparten un post
    POST_FROM_FOLLOWING = "post_from_following"  # Cuando una mascota que sigues publica
    COMMENT_REPLY = "comment_reply"      # Respuestas a comentarios
    SYSTEM = "system"                    # Notificaciones del sistema

class NotificationBase(BaseModel):
    user_id: int = Field(..., description="ID del usuario que recibirá la notificación")
    type: NotificationType = Field(..., description="Tipo de notificación")
    related_id: Optional[int] = Field(None, description="ID del objeto relacionado (post, comentario, etc.)")
    message: Optional[str] = Field(None, description="Mensaje personalizado de la notificación")
    additional_data: Optional[Dict[str, Any]] = Field(
        None,
        description="Datos adicionales específicos del tipo de notificación"
    )

class NotificationCreate(NotificationBase):
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": 1,
                "type": "NEW_FOLLOWER",
                "related_id": 123,
                "message": "Max comenzó a seguirte",
                "additional_data": {
                    "follower_name": "Max",
                    "follower_picture": "path/to/picture.jpg"
                }
            }
        }

class NotificationUpdate(BaseModel):
    is_read: bool = Field(True, description="Estado de lectura de la notificación")
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class NotificationContext(BaseModel):
    """Información de contexto para diferentes tipos de notificaciones"""
    title: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    link: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class NotificationResponse(NotificationBase):
    notification_id: int
    is_read: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    context: Optional[NotificationContext] = None
    
    # Campos específicos por tipo de notificación
    related_pet_name: Optional[str] = None
    related_pet_picture: Optional[str] = None
    related_post_preview: Optional[str] = None
    related_post_id: Optional[int] = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "notification_id": 1,
                "user_id": 1,
                "type": "NEW_FOLLOWER",
                "related_id": 123,
                "message": "Max comenzó a seguirte",
                "is_read": False,
                "created_at": "2024-10-25T14:30:00",
                "context": {
                    "title": "Nuevo seguidor",
                    "description": "Max ahora te sigue",
                    "image_url": "path/to/picture.jpg",
                    "link": "/pets/123"
                }
            }
        }
    )

class NotificationTypeCount(BaseModel):
    type: NotificationType
    count: int
    unread_count: int

class NotificationCount(BaseModel):
    total: int = Field(..., description="Total de notificaciones")
    unread: int = Field(..., description="Total de notificaciones no leídas")
    by_type: Dict[NotificationType, int] = Field(
        ..., 
        description="Conteo de notificaciones por tipo"
    )
    type_details: Optional[List[NotificationTypeCount]] = Field(
        None,
        description="Detalles de conteo por tipo incluyendo leídas/no leídas"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "total": 10,
                "unread": 3,
                "by_type": {
                    "NEW_FOLLOWER": 2,
                    "NEW_COMMENT": 5,
                    "NEW_REACTION": 3
                },
                "type_details": [
                    {
                        "type": "NEW_FOLLOWER",
                        "count": 2,
                        "unread_count": 1
                    }
                ]
            }
        }

class NotificationFilter(BaseModel):
    """Filtros para búsqueda de notificaciones"""
    notification_type: Optional[NotificationType] = None
    is_read: Optional[bool] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    related_id: Optional[int] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "notification_type": "NEW_FOLLOWER",
                "is_read": False,
                "start_date": "2024-10-20T00:00:00",
                "end_date": "2024-10-25T23:59:59"
            }
        }