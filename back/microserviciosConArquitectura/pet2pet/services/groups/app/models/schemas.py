from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime

class GroupBase(BaseModel):
    name_group: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    privacy: bool = Field(True, description="True for private, False for public")

class GroupCreate(GroupBase):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name_group": "Dog Lovers Club",
                "description": "A group for dog lovers to share experiences",
                "privacy": True
            }
        }
    )

class GroupUpdate(BaseModel):
    name_group: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    privacy: Optional[bool] = None
    group_picture: Optional[str] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name_group": "Updated Dog Lovers Club",
                "description": "Updated description",
                "privacy": False
            }
        }
    )

class GroupMemberBase(BaseModel):
    pet_id: Optional[int] = None
    admin: bool = False

class GroupMemberCreate(GroupMemberBase):
    pass

class GroupMemberResponse(GroupMemberBase):
    member_id: int
    user_id: int
    group_id: int
    joined_at: datetime
    pet_name: Optional[str] = None
    user_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class GroupResponse(GroupBase):
    group_id: int
    owner_id: int
    created_at: datetime
    group_picture: Optional[str] = None
    member_count: int
    is_member: bool
    is_admin: bool
    owner_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class GroupPostBase(BaseModel):
    content: str = Field(..., min_length=1, max_length=1000)

class GroupPostCreate(GroupPostBase):
    pass

class GroupPostUpdate(BaseModel):
    content: Optional[str] = Field(None, min_length=1, max_length=1000)

class GroupPostResponse(GroupPostBase):
    group_post_id: int
    group_id: int
    user_id: int
    pet_id: Optional[int]
    created_at: datetime
    user_name: Optional[str] = None
    pet_name: Optional[str] = None
    media_urls: List[str] = []

    model_config = ConfigDict(from_attributes=True)

class GroupCommentBase(BaseModel):
    comment: str = Field(..., min_length=1, max_length=500)

class GroupCommentCreate(GroupCommentBase):
    pass

class GroupCommentResponse(GroupCommentBase):
    group_comment_id: int
    group_post_id: int
    user_id: int
    pet_id: Optional[int]
    created_at: datetime
    user_name: Optional[str] = None
    pet_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)