# services/auth/app/models/schemas.py
from pydantic import BaseModel, EmailStr, constr, Field
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    user_name: constr(min_length=2, max_length=100) # type: ignore
    user_last_name: constr(min_length=2, max_length=100) # type: ignore
    user_email: EmailStr
    user_city: Optional[str] = None
    user_country: Optional[str] = None
    user_number: Optional[str] = None
    user_bio: Optional[str] = None
    role_id: Optional[int] = None 

class UserCreate(UserBase):
    password: constr(min_length=8) # type: ignore

class UserUpdate(BaseModel):
    user_name: Optional[str] = Field(None, min_length=2, max_length=100)
    user_last_name: Optional[str] = Field(None, min_length=2, max_length=100)
    user_email: Optional[EmailStr] = None
    user_city: Optional[str] = None
    user_country: Optional[str] = None
    user_number: Optional[str] = None
    user_bio: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "user_name": "John",
                "user_last_name": "Doe",
                "user_email": "johndoe@example.com",  
                "user_city": "New York",
                "user_country": "USA",
                "user_number": "123456789",
                "user_bio": "I love pets more dogs than cats!"
            }
        }

class UserInDB(UserBase):
    user_id: int
    is_active: bool = True
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class UserResponse(UserBase):
    user_id: int
    profile_picture: Optional[str] = None
    is_active: bool = True

    class Config:
        from_attributes = True
        populated_by_name = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse

    class Config:
        from_attributes = True

class TokenData(BaseModel):
    user_id: Optional[int] = None
    email: Optional[str] = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: constr(min_length=8) # type: ignore

class RequestPasswordReset(BaseModel):
    email: EmailStr

class ResetPassword(BaseModel):
    token: str
    new_password: constr(min_length=8) # type: ignore