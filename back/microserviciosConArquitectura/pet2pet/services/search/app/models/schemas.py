from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any, Union
from datetime import datetime
from enum import Enum

class SearchType(str, Enum):
    ALL = "all"
    PETS = "pets"
    USERS = "users"
    POSTS = "posts"
    GROUPS = "groups"
    COMMENTS = "comments"

class SortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"

class SearchFilters(BaseModel):
    type: SearchType = Field(default=SearchType.ALL, description="Tipo de contenido a buscar")
    breed_id: Optional[int] = Field(None, description="Filtrar mascotas por raza")
    pet_type_id: Optional[int] = Field(None, description="Filtrar por tipo de mascota")
    location: Optional[str] = Field(None, description="Filtrar por ubicación")
    date_from: Optional[datetime] = Field(None, description="Fecha inicial para la búsqueda")
    date_to: Optional[datetime] = Field(None, description="Fecha final para la búsqueda")
    status: Optional[bool] = Field(None, description="Filtrar por estado activo/inactivo")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "type": "pets",
                "breed_id": 1,
                "pet_type_id": 1,
                "location": "New York",
                "date_from": "2024-01-01T00:00:00",
                "status": True
            }
        }
    )

class SearchQuery(BaseModel):
    query: str = Field(..., min_length=1, description="Término de búsqueda")
    filters: Optional[SearchFilters] = Field(default_factory=SearchFilters)
    sort_by: Optional[str] = Field(None, description="Campo por el cual ordenar")
    sort_order: Optional[SortOrder] = Field(default=SortOrder.DESC)
    page: int = Field(default=1, ge=1, description="Número de página")
    page_size: int = Field(default=10, ge=1, le=100, description="Resultados por página")

class PetResult(BaseModel):
    pet_id: int
    name: str
    pet_picture: Optional[str]
    breed_name: Optional[str]
    pet_type: Optional[str]
    user_id: int
    owner_name: str
    score: float

class UserResult(BaseModel):
    user_id: int
    user_name: str
    user_last_name: str
    profile_picture: Optional[str]
    pet_count: int
    score: float

class PostResult(BaseModel):
    post_id: int
    content: str
    user_id: int
    pet_id: Optional[int]
    created_at: datetime
    media_urls: List[str]
    author_name: str
    pet_name: Optional[str]
    score: float

class GroupResult(BaseModel):
    group_id: int
    name_group: str
    description: Optional[str]
    group_picture: Optional[str]
    member_count: int
    privacy: bool
    score: float

class CommentResult(BaseModel):
    comment_id: int
    content: str
    post_id: int
    user_id: int
    pet_id: Optional[int]
    created_at: datetime
    author_name: str
    score: float

class SearchResult(BaseModel):
    pets: List[PetResult] = Field(default_factory=list)
    users: List[UserResult] = Field(default_factory=list)
    posts: List[PostResult] = Field(default_factory=list)
    groups: List[GroupResult] = Field(default_factory=list)
    comments: List[CommentResult] = Field(default_factory=list)
    total_results: int
    page: int
    total_pages: int
    search_time: float  # tiempo en segundos
    suggestions: List[str] = Field(default_factory=list)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "pets": [
                    {
                        "pet_id": 1,
                        "name": "Max",
                        "pet_picture": "url/to/picture.jpg",
                        "breed_name": "Labrador",
                        "pet_type": "Dog",
                        "user_id": 1,
                        "owner_name": "John Doe",
                        "score": 0.95
                    }
                ],
                "total_results": 1,
                "page": 1,
                "total_pages": 1,
                "search_time": 0.05,
                "suggestions": ["maxi", "maxwell"]
            }
        }
    )