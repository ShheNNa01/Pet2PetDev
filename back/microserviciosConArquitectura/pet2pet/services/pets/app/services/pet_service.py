# services/pets/app/services/pet_service.py
from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from services.pets.app.services.file_service import FileService
from shared.database.models import Pet, User, PetType, Breed
from services.pets.app.models.schemas import PetCreate, PetUpdate, PetFilter

class PetService:
    @staticmethod
    async def create_pet(db: Session, user_id: int, pet_data: PetCreate) -> Pet:
        try:
            # Verificar límite de mascotas por usuario
            user_pets_count = db.query(Pet).filter(Pet.user_id == user_id).count()
            if user_pets_count >= 5:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Maximum number of pets reached"
                )

            # Validar breed_id si se proporciona
            if pet_data.breed_id:
                breed = db.query(Breed).filter(Breed.breed_id == pet_data.breed_id).first()
                if not breed:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Breed not found"
                    )

            # Crear el objeto Pet con los datos
            db_pet = Pet(
                user_id=user_id,
                name=pet_data.name,
                breed_id=pet_data.breed_id,
                birthdate=pet_data.birthdate,
                gender=pet_data.gender,
                bio=pet_data.bio,
                status=True
            )

            print(f"Creating pet with data: {db_pet.__dict__}")  # Para debugging

            # Añadir y guardar en la base de datos
            db.add(db_pet)
            db.commit()
            db.refresh(db_pet)
        
            return db_pet

        except Exception as e:
            db.rollback()
            print(f"Error in create_pet: {str(e)}")  # Para debugging
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating pet: {str(e)}"
            )

    @staticmethod
    async def get_pet(db: Session, pet_id: int) -> Pet:
        pet = db.query(Pet).filter(Pet.pet_id == pet_id).first()
        if not pet:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pet not found"
            )
        return pet

    @staticmethod
    async def get_pets(
        db: Session,
        skip: int = 0,
        limit: int = 10,
        filters: Optional[PetFilter] = None
    ) -> List[Pet]:
        query = db.query(Pet)

        if filters:
            if filters.pet_type_id:
                query = query.join(Breed).filter(Breed.pet_type_id == filters.pet_type_id)
            if filters.breed_id:
                query = query.filter(Pet.breed_id == filters.breed_id)
            if filters.gender:
                query = query.filter(Pet.gender == filters.gender)
            if filters.name:
                query = query.filter(Pet.name.ilike(f"%{filters.name}%"))

        return query.offset(skip).limit(limit).all()

    @staticmethod
    async def update_pet(
        db: Session,
        user_id: int,
        pet_id: int,
        pet_data: PetUpdate
    ) -> Pet:
        pet = db.query(Pet).filter(
            Pet.pet_id == pet_id,
            Pet.user_id == user_id
        ).first()

        if not pet:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pet not found or you don't have permission to update it"
            )

        # Validar breed_id si se proporciona
        if pet_data.breed_id:
            breed = db.query(Breed).filter(Breed.breed_id == pet_data.breed_id).first()
            if not breed:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Breed not found"
                )

        # Actualizar campos
        for field, value in pet_data.dict(exclude_unset=True).items():
            setattr(pet, field, value)
        
        pet.updated_at = datetime.utcnow()

        try:
            db.commit()
            db.refresh(pet)
            return pet
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error updating pet: {str(e)}"
            )

    @staticmethod
    async def delete_pet(db: Session, user_id: int, pet_id: int) -> None:
        pet = db.query(Pet).filter(
            Pet.pet_id == pet_id,
            Pet.user_id == user_id
        ).first()

        if not pet:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pet not found or you don't have permission to delete it"
            )

        try:
            # Eliminar imagen si existe
            if pet.pet_picture:
                await FileService.delete_pet_image(pet.pet_picture)

            # Eliminar mascota
            db.delete(pet)
            db.commit()
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error deleting pet: {str(e)}"
            )