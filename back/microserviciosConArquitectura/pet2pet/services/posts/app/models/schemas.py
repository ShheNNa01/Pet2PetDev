from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime

class CommentBase(BaseModel):
    comment: str = Field(..., min_length=1, max_length=500)
    media_url: Optional[str] = None

class CommentCreate(CommentBase):
    pet_id: int

class CommentResponse(CommentBase):
    comment_id: int
    post_id: int
    user_id: int
    pet_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class PostBase(BaseModel):
    content: str = Field(..., min_length=1, max_length=1000)
    location: Optional[str] = None
    pet_id: int

class PostCreate(BaseModel):
    content: str
    location: str
    pet_id: int

class PostUpdate(BaseModel):
    content: Optional[str] = Field(None, min_length=1, max_length=1000)
    location: Optional[str] = None

class PostResponse(BaseModel):
    post_id: int
    content: str
    location: Optional[str] = None
    pet_id: int
    user_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    media_urls: List[str] = []
    comments_count: int = 0
    reactions_count: int = 0
    comments: List[CommentResponse] = []

    model_config = ConfigDict(from_attributes=True)

class ReactionBase(BaseModel):
    reaction_type: str = Field(..., pattern="^(like|love|laugh|wow|sad|angry)$")
    pet_id: int

class ReactionCreate(ReactionBase):
    pass

class ReactionResponse(ReactionBase):
    reaction_id: int
    post_id: int
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class PostFilter(BaseModel):
    user_id: Optional[int] = None
    pet_id: Optional[int] = None
    location: Optional[str] = None
    from_date: Optional[datetime] = None
    to_date: Optional[datetime] = None
    has_media: Optional[bool] = None