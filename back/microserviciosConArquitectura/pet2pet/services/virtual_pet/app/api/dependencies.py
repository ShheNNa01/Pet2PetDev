# services/virtual_pet/app/api/dependencies.py
from typing import Generator
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from services.virtual_pet.app.services.virtual_pet_service import VirtualPetService
from shared.database.session import get_db
from shared.config.settings import settings

async def get_virtual_pet_service(db: Session = Depends(get_db)) -> VirtualPetService:
    return VirtualPetService()

