# services/virtual_pet/app/api/routes.py
from fastapi import APIRouter
from services.virtual_pet.app.api.endpoints import router as virtualPetRouter

api_router = APIRouter()
api_router.include_router(virtualPetRouter, tags=["posts"])