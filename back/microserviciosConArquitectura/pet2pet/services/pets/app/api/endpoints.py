# services/pets/app/api/endpoints.py
from datetime import datetime
import os
import uuid
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from shared.database.session import get_db
from shared.database.models import Pet, User
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
    db: Session = Depends(get_db)
):
    """
    Upload a pet image
    """
    # Verificar que la mascota existe y pertenece al usuario
    pet = db.query(Pet).filter(
        Pet.pet_id == pet_id,
        Pet.user_id == current_user.user_id
    ).first()
    
    if not pet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pet not found or not authorized"
        )

    try:
        # Crear directorio si no existe
        media_directory = "uploads/pets"
        if not os.path.exists(media_directory):
            os.makedirs(media_directory)

        # Validar extensión
        file_extension = os.path.splitext(file.filename)[1].lower()
        if file_extension not in ['.jpg', '.jpeg', '.png']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid file extension. Only .jpg, .jpeg and .png are allowed"
            )

        # Generar nombre único
        unique_filename = f"{pet_id}_{uuid.uuid4()}{file_extension}"
        file_location = os.path.join(media_directory, unique_filename)
        
        # Guardar archivo
        with open(file_location, "wb") as buffer:
            content = await file.read()
            buffer.write(content)

        # Actualizar la ruta de la imagen en la base de datos
        pet.pet_picture = file_location
        pet.updated_at = datetime.utcnow()  # Usar datetime.utcnow() en lugar de 'CURRENT_TIMESTAMP'
        db.commit()
        
        return pet

    except Exception as e:
        # Si algo sale mal, eliminar el archivo si se creó
        if 'file_location' in locals() and os.path.exists(file_location):
            os.remove(file_location)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error uploading image: {str(e)}"
        )

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
    Get all pets from the current user
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