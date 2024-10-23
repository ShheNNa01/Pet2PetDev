# services/pets/app/api/endpoints.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from shared.database.session import get_db
from shared.database.models import User
from services.pets.app.models.schemas import (
    PetCreate, PetResponse, PetUpdate, PetFilter,
    PetTypeResponse, BreedResponse
)
from services.pets.app.services.pet_service import PetService
from services.pets.app.api.dependencies import get_current_active_user, get_pet_service
from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi import UploadFile, File
from services.pets.app.services.file_service import FileService

router = APIRouter()

@router.post("/", response_model=PetResponse, status_code=status.HTTP_201_CREATED)
async def create_pet(
    pet_data: PetCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
    pet_service: PetService = Depends(get_pet_service)
):
    """
    Create a new pet for the current user.
    """
    try:
        result = await pet_service.create_pet(db, current_user.user_id, pet_data)
        return result
    except Exception as e:
        print(f"Error creating pet: {str(e)}")  # Para debugging
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating pet: {str(e)}"
        )
    
@router.post("/{pet_id}/image", response_model=PetResponse)
async def upload_pet_image(
    pet_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
    pet_service: PetService = Depends(get_pet_service)
):
    """
    Upload a pet image
    """
    # Verificar que la mascota existe y pertenece al usuario
    pet = await pet_service.get_pet(db, pet_id)
    if pet.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this pet"
        )

    # Guardar la imagen
    image_path = await FileService.save_pet_image(file, pet_id)

    # Actualizar la ruta de la imagen en la mascota
    pet.pet_picture = image_path
    db.commit()
    db.refresh(pet)

    return pet

@router.get("/", response_model=List[PetResponse])
async def get_pets(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    name: Optional[str] = None,
    pet_type_id: Optional[int] = None,
    breed_id: Optional[int] = None,
    gender: Optional[str] = None,
    db: Session = Depends(get_db),
    pet_service: PetService = Depends(get_pet_service)
):
    """
    Get all pets with optional filters.
    """
    filters = PetFilter(
        name=name,
        pet_type_id=pet_type_id,
        breed_id=breed_id,
        gender=gender
    )
    return await pet_service.get_pets(db, skip, limit, filters)

@router.get("/my-pets", response_model=List[PetResponse])
async def get_my_pets(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
    pet_service: PetService = Depends(get_pet_service)
):
    """
    Get all pets belonging to the current user.
    """
    return await pet_service.get_user_pets(db, current_user.user_id, skip, limit)

@router.get("/{pet_id}", response_model=PetResponse)
async def get_pet(
    pet_id: int,
    db: Session = Depends(get_db),
    pet_service: PetService = Depends(get_pet_service)
):
    """
    Get a specific pet by ID.
    """
    return await pet_service.get_pet(db, pet_id)

@router.put("/{pet_id}", response_model=PetResponse)
async def update_pet(
    pet_id: int,
    pet_data: PetUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
    pet_service: PetService = Depends(get_pet_service)
):
    """
    Update a pet belonging to the current user.
    """
    return await pet_service.update_pet(db, current_user.user_id, pet_id, pet_data)

@router.delete("/{pet_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_pet(
    pet_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
    pet_service: PetService = Depends(get_pet_service)
):
    """
    Delete a pet belonging to the current user.
    """
    await pet_service.delete_pet(db, current_user.user_id, pet_id)
    return {"status": "success"}

@router.get("/types", response_model=List[PetTypeResponse])
async def get_pet_types(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    pet_service: PetService = Depends(get_pet_service)
):
    """
    Get all pet types.
    """
    return await pet_service.get_pet_types(db, skip, limit)

@router.get("/breeds", response_model=List[BreedResponse])
async def get_breeds(
    pet_type_id: Optional[int] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    pet_service: PetService = Depends(get_pet_service)
):
    """
    Get all breeds, optionally filtered by pet type.
    """
    return await pet_service.get_breeds(db, pet_type_id, skip, limit)