from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime

class MessageBase(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000)

class MessageCreate(MessageBase):
    receiver_pet_id: int

class MessageUpdate(BaseModel):
    read_status: bool = Field(default=True)

class MessageResponse(MessageBase):
    message_id: int
    sender_pet_id: int
    receiver_pet_id: int
    created_at: datetime
    read_status: bool

    model_config = ConfigDict(from_attributes=True)

class ConversationResponse(BaseModel):
    pet_id: int
    pet_name: str
    pet_picture: Optional[str]
    last_message: str
    last_message_time: datetime
    unread_count: int
    
    model_config = ConfigDict(from_attributes=True)