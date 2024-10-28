from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class FeedType(str, Enum):
    MAIN = "main"            # Feed principal con todo el contenido
    FOLLOWING = "following"  # Solo de mascotas seguidas
    GROUPS = "groups"        # Solo posts de grupos
    TRENDING = "trending"    # Contenido popular
    NEARBY = "nearby"        # Contenido por ubicación

class ContentType(str, Enum):
    POST = "post"
    GROUP_POST = "group_post"
    PET_ACTION = "pet_action"         # Nuevas mascotas seguidas, amistades, etc.
    GROUP_ACTION = "group_action"     # Nuevos miembros, cambios en grupo, etc.
    SYSTEM = "system"                 # Anuncios del sistema, eventos, etc.

class MediaContent(BaseModel):
    media_id: int
    media_url: str
    media_type: str
    thumbnail_url: Optional[str] = None

class UserPreview(BaseModel):
    user_id: int
    user_name: str
    profile_picture: Optional[str] = None

class PetPreview(BaseModel):
    pet_id: int
    name: str
    pet_picture: Optional[str] = None
    breed_name: Optional[str] = None

class GroupPreview(BaseModel):
    group_id: int
    name_group: str
    group_picture: Optional[str] = None

class FeedItemStats(BaseModel):
    likes_count: int = 0
    comments_count: int = 0
    shares_count: int = 0

class FeedItem(BaseModel):
    item_id: str  # Identificador único para el item del feed
    content_type: ContentType
    created_at: datetime
    relevance_score: float
    
    # Campos específicos según el tipo de contenido
    content: Dict[str, Any]  # Contenido específico del item
    user: UserPreview
    pet: Optional[PetPreview] = None
    group: Optional[GroupPreview] = None
    media: List[MediaContent] = []
    stats: FeedItemStats
    location: Optional[str] = None
    is_liked: bool = False
    is_shared: bool = False
    tags: List[str] = []

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "item_id": "post_123",
                "content_type": "post",
                "created_at": "2024-10-25T14:30:00",
                "relevance_score": 0.95,
                "content": {
                    "text": "¡Un día increíble en el parque!",
                    "location": "Central Park"
                },
                "user": {
                    "user_id": 1,
                    "user_name": "John Doe",
                    "profile_picture": "url/to/picture.jpg"
                },
                "pet": {
                    "pet_id": 1,
                    "name": "Max",
                    "pet_picture": "url/to/picture.jpg",
                    "breed_name": "Labrador"
                },
                "media": [
                    {
                        "media_id": 1,
                        "media_url": "url/to/media.jpg",
                        "media_type": "image",
                        "thumbnail_url": "url/to/thumbnail.jpg"
                    }
                ],
                "stats": {
                    "likes_count": 15,
                    "comments_count": 3,
                    "shares_count": 1
                },
                "is_liked": False,
                "is_shared": False,
                "tags": ["parque", "perros", "diversión"]
            }
        }
    )

class FeedFilters(BaseModel):
    feed_type: FeedType = Field(default=FeedType.MAIN)
    content_types: Optional[List[ContentType]] = None
    pet_id: Optional[int] = None
    group_id: Optional[int] = None
    location: Optional[str] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    tags: Optional[List[str]] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "feed_type": "following",
                "content_types": ["post", "group_post"],
                "pet_id": 1,
                "location": "New York",
                "tags": ["perros", "parque"]
            }
        }
    )

class FeedResponse(BaseModel):
    items: List[FeedItem]
    total_items: int
    page: int
    total_pages: int
    has_more: bool
    next_cursor: Optional[str] = None
    feed_type: FeedType
    processing_time: float  # tiempo en segundos

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "items": [],  # Lista de FeedItems
                "total_items": 100,
                "page": 1,
                "total_pages": 10,
                "has_more": True,
                "next_cursor": "timestamp_123456",
                "feed_type": "main",
                "processing_time": 0.05
            }
        }
    )

class FeedPreferences(BaseModel):
    preferred_content_types: List[ContentType] = Field(
        default_factory=lambda: list(ContentType),
        description="Tipos de contenido preferidos"
    )
    following_only: bool = Field(
        default=False,
        description="Mostrar solo contenido de mascotas seguidas"
    )
    location_based: bool = Field(
        default=True,
        description="Mostrar contenido basado en ubicación"
    )
    language: Optional[str] = Field(
        default="es",
        description="Idioma preferido para el contenido"
    )
    excluded_tags: List[str] = Field(
        default_factory=list,
        description="Tags a excluir del feed"
    )
    content_sensitivity: str = Field(
        default="normal",
        description="Nivel de sensibilidad del contenido"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "preferred_content_types": ["post", "group_post"],
                "following_only": False,
                "location_based": True,
                "language": "es",
                "excluded_tags": ["nsfw"],
                "content_sensitivity": "normal"
            }
        }
    )

class FeedAction(BaseModel):
    action_type: str = Field(..., description="Tipo de acción (like, share, hide, etc.)")
    item_id: str = Field(..., description="ID del item del feed")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "action_type": "like",
                "item_id": "post_123",
                "timestamp": "2024-10-25T14:30:00",
                "metadata": {
                    "source": "feed",
                    "device": "mobile"
                }
            }
        }
    )