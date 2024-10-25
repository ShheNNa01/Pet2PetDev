from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
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
    user_id: int
    type: NotificationType
    related_id: Optional[int] = None
    message: Optional[str] = None

class NotificationCreate(NotificationBase):
    pass

class NotificationUpdate(BaseModel):
    is_read: bool = True

class NotificationResponse(NotificationBase):
    notification_id: int
    is_read: bool
    created_at: datetime
    # Campos adicionales para información contextual
    related_pet_name: Optional[str] = None
    related_post_preview: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class NotificationCount(BaseModel):
    total: int
    unread: int
    by_type: dict[NotificationType, int]  # Conteo por tipo de notificación