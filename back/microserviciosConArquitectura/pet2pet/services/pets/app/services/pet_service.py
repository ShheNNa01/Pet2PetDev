from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from services.pets.app.services.file_service import FileService
from shared.database.models import Pet, User, PetType, Breed, Follower
from services.pets.app.models.schemas import PetCreate, PetUpdate, PetFilter
from services.notifications.app.services.notification_service import NotificationService
from services.notifications.app.models.schemas import NotificationType

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

            # Añadir y guardar en la base de datos
            db.add(db_pet)
            db.commit()
            db.refresh(db_pet)
        
            return db_pet

        except Exception as e:
            db.rollback()
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
        
    @staticmethod
    async def get_user_pets(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Pet]:
        """
        Obtener todas las mascotas de un usuario específico
        """
        try:
            pets = db.query(Pet).filter(
                Pet.user_id == user_id,
                Pet.status == True  # Solo mascotas activas
            ).offset(skip).limit(limit).all()
            
            return pets
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error getting user pets: {str(e)}"
            )

    @staticmethod
    async def follow_pet(db: Session, follower_pet_id: int, followed_pet_id: int) -> Follower:
        """
        Seguir a una mascota
        """
        try:
            # Verificar que las mascotas existen
            follower_pet = db.query(Pet).filter(Pet.pet_id == follower_pet_id).first()
            followed_pet = db.query(Pet).filter(Pet.pet_id == followed_pet_id).first()

            if not follower_pet or not followed_pet:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="One or both pets not found"
                )

            # Verificar que no se está siguiendo a sí mismo
            if follower_pet_id == followed_pet_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Cannot follow yourself"
                )

            # Verificar si ya sigue a la mascota
            existing_follow = db.query(Follower).filter(
                Follower.follower_pet_id == follower_pet_id,
                Follower.followed_pet_id == followed_pet_id
            ).first()

            if existing_follow:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Already following this pet"
                )

            # Crear nuevo seguidor
            new_follower = Follower(
                follower_pet_id=follower_pet_id,
                followed_pet_id=followed_pet_id
            )
            
            db.add(new_follower)

            # Crear notificación para el dueño de la mascota seguida
            await NotificationService.create_notification_for_event(
                db=db,
                event_type=NotificationType.NEW_FOLLOWER,
                user_id=followed_pet.user_id,
                related_id=follower_pet_id,
                custom_message=f"{follower_pet.name} ha comenzado a seguir a {followed_pet.name}"
            )

            db.commit()
            return new_follower

        except HTTPException as e:
            raise e
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error following pet: {str(e)}"
            )

    @staticmethod
    async def unfollow_pet(db: Session, follower_pet_id: int, followed_pet_id: int) -> None:
        """
        Dejar de seguir a una mascota
        """
        try:
            follow = db.query(Follower).filter(
                Follower.follower_pet_id == follower_pet_id,
                Follower.followed_pet_id == followed_pet_id
            ).first()

            if not follow:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Not following this pet"
                )

            db.delete(follow)
            db.commit()

        except HTTPException as e:
            raise e
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error unfollowing pet: {str(e)}"
            )

    @staticmethod
    async def get_followers(db: Session, pet_id: int, skip: int = 0, limit: int = 100) -> List[Pet]:
        """
        Obtener todos los seguidores de una mascota
        """
        try:
            followers = db.query(Pet).join(
                Follower, Follower.follower_pet_id == Pet.pet_id
            ).filter(
                Follower.followed_pet_id == pet_id
            ).offset(skip).limit(limit).all()

            return followers

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error getting followers: {str(e)}"
            )

    @staticmethod
    async def get_following(db: Session, pet_id: int, skip: int = 0, limit: int = 100) -> List[Pet]:
        """
        Obtener todas las mascotas que sigue una mascota
        """
        try:
            following = db.query(Pet).join(
                Follower, Follower.followed_pet_id == Pet.pet_id
            ).filter(
                Follower.follower_pet_id == pet_id
            ).offset(skip).limit(limit).all()

            return following

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error getting following: {str(e)}"
            )