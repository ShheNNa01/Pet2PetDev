from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict
from datetime import datetime

class MessageBase(BaseModel):
    receiver_pet_id: int = Field(..., description="ID de la mascota que recibirá el mensaje")
    message: str = Field(..., min_length=1, max_length=1000, description="Contenido del mensaje")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "receiver_pet_id": 1,
                "message": "¡Hola! ¿Cómo estás?"
            }
        }
    )

class MessageCreate(MessageBase):
    pass

class MessageUpdate(BaseModel):
    read_status: bool = Field(True, description="Estado de lectura del mensaje")

class PetInfo(BaseModel):
    pet_id: int
    name: str
    pet_picture: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class MessageResponse(MessageBase):
    message_id: int
    sender_pet_id: int
    created_at: datetime
    read_status: bool
    sender_pet: Optional[PetInfo] = None
    receiver_pet: Optional[PetInfo] = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "message_id": 1,
                "sender_pet_id": 2,
                "receiver_pet_id": 1,
                "message": "¡Hola! ¿Cómo estás?",
                "created_at": "2024-10-25T14:30:00",
                "read_status": False,
                "sender_pet": {
                    "pet_id": 2,
                    "name": "Max",
                    "pet_picture": "path/to/picture.jpg"
                },
                "receiver_pet": {
                    "pet_id": 1,
                    "name": "Luna",
                    "pet_picture": "path/to/picture.jpg"
                }
            }
        }
    )

class LastMessage(BaseModel):
    message_id: int
    message: str
    created_at: datetime
    read_status: bool

    model_config = ConfigDict(from_attributes=True)

class ConversationResponse(BaseModel):
    other_pet: PetInfo
    last_message: LastMessage
    unread_count: int

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "other_pet": {
                    "pet_id": 2,
                    "name": "Max",
                    "pet_picture": "path/to/picture.jpg"
                },
                "last_message": {
                    "message_id": 1,
                    "message": "¡Hola! ¿Cómo estás?",
                    "created_at": "2024-10-25T14:30:00",
                    "read_status": False
                },
                "unread_count": 3
            }
        }
    )

class UnreadCountResponse(BaseModel):
    total_unread: int = Field(..., description="Total de mensajes no leídos")
    conversations_with_unread: int = Field(..., description="Número de conversaciones con mensajes no leídos")
    unread_by_conversation: Dict[int, int] = Field(
        ..., 
        description="Conteo de mensajes no leídos por conversación (pet_id: count)"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "total_unread": 5,
                "conversations_with_unread": 2,
                "unread_by_conversation": {
                    "1": 2,
                    "2": 3
                }
            }
        }
    )

class MessageSearchResult(BaseModel):
    messages: List[MessageResponse]
    total_count: int
    page: int
    total_pages: int

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "messages": [
                    {
                        "message_id": 1,
                        "sender_pet_id": 2,
                        "receiver_pet_id": 1,
                        "message": "¡Hola! ¿Cómo estás?",
                        "created_at": "2024-10-25T14:30:00",
                        "read_status": False
                    }
                ],
                "total_count": 1,
                "page": 1,
                "total_pages": 1
            }
        }
    )