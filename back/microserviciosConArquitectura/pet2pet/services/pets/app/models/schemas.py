# services/pets/app/models/schemas.py
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import date, datetime

class PetTypeBase(BaseModel):
    type_name: str = Field(..., min_length=2, max_length=30)

class PetTypeCreate(PetTypeBase):
    pass

class PetTypeResponse(BaseModel):
    pet_type_id: int
    type_name: str
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "pet_type_id": 1,
                "type_name": "Dog",
                "created_at": "2024-10-25T14:30:00"
            }
        }
    )

class BreedBase(BaseModel):
    breed_name: str = Field(..., min_length=2, max_length=30)
    pet_type_id: int

class BreedCreate(BreedBase):
    pass

class BreedResponse(BaseModel):
    breed_id: int
    breed_name: str
    pet_type_id: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "breed_id": 1,
                "breed_name": "Labrador Retriever",
                "pet_type_id": 1,
                "created_at": "2024-10-25T14:30:00"
            }
        }
    )

class PetBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    breed_id: Optional[int] = None
    birthdate: Optional[date] = None
    gender: Optional[str] = Field(None, pattern="^(male|female)$")
    bio: Optional[str] = Field(None, max_length=200)

class PetCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    breed_id: Optional[int] = None
    birthdate: Optional[date] = None
    gender: Optional[str] = Field(None, pattern="^(male|female)$")
    bio: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Max",
                "breed_id": 1,
                "birthdate": "2023-01-01",
                "gender": "male",
                "bio": "Friendly dog"
            }
        }

class PetUpdate(PetBase):
    name: Optional[str] = Field(None, min_length=2, max_length=50)
    status: Optional[bool] = None

class PetResponse(PetBase):
    pet_id: int
    user_id: int
    pet_picture: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    status: bool

    model_config = ConfigDict(from_attributes=True)

class PetFilter(BaseModel):
    pet_type_id: Optional[int] = None
    breed_id: Optional[int] = None
    gender: Optional[str] = None
    min_age: Optional[int] = None
    max_age: Optional[int] = None
    name: Optional[str] = None