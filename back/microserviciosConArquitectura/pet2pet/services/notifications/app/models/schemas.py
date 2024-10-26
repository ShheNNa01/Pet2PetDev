from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict, Any
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
    GROUP_INVITE = "group_invite"         # Para invitaciones a grupos
    GROUP_JOIN_REQUEST = "group_join_request"   # Para solicitudes de unirse a un grupo
    GROUP_MEMBER_JOINED = "group_member_joined"   # Para cuando un miembro se une a un grupo
    GROUP_MEMBER_LEFT = "group_member_left"      # Para cuando un miembro sale de un grupo
    GROUP_MEMBER_REMOVED = "group_member_removed"   # Para cuando un miembro es removido de un grupo
    GROUP_ROLE_CHANGED = "group_role_changed"       # Para cuando un miembro cambia de rol en un grupo
    GROUP_POST_NEW = "group_post_new"               # Para nuevos posts en grupos
    GROUP_POST_COMMENT = "group_post_comment"        # Para comentarios en posts de grupos
    GROUP_OWNERSHIP_TRANSFER = "group_ownership_transfer"   # Para cuando se transfieren los derechos de un grupo
    GROUP_SETTINGS_CHANGED = "group_settings_changed"      # Para cuando se cambian los ajustes de un grupo


class NotificationBase(BaseModel):
    user_id: int = Field(..., description="ID del usuario que recibirá la notificación")
    type: NotificationType = Field(..., description="Tipo de notificación")
    related_id: Optional[int] = Field(None, description="ID del objeto relacionado (post, comentario, etc.)")
    message: str = Field(..., min_length=1, description="Mensaje de la notificación")
    additional_data: Optional[Dict[str, Any]] = Field(None, description="Datos adicionales de la notificación")

class NotificationCreate(NotificationBase):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "user_id": 1,
                "type": "NEW_FOLLOWER",
                "related_id": 123,
                "message": "Max comenzó a seguirte",
                "additional_data": {
                    "follower_pet_id": 456,
                    "follower_pet_name": "Max"
                }
            }
        }
    )

class NotificationUpdate(BaseModel):
    is_read: bool = Field(default=True, description="Estado de lectura de la notificación")

class NotificationResponse(NotificationBase):
    notification_id: int
    is_read: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

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
                "additional_data": {
                    "follower_pet_id": 456,
                    "follower_pet_name": "Max"
                }
            }
        }
    )

class NotificationCount(BaseModel):
    total: int = Field(..., description="Total de notificaciones")
    unread: int = Field(..., description="Notificaciones no leídas")
    by_type: Dict[NotificationType, int] = Field(
        default_factory=dict,
        description="Conteo por tipo de notificación"
    )