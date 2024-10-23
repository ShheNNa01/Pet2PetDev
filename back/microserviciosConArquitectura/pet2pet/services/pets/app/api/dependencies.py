# services/pets/app/api/dependencies.py
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from shared.database.session import get_db
from shared.database.models import User
from services.pets.app.services.pet_service import PetService
from services.auth.app.api.dependencies import get_current_user

def get_pet_service() -> PetService:
    return PetService()

async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.status:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user