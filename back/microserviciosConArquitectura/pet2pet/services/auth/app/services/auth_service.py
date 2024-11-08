# services/auth/app/services/auth_service.py
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from shared.constants.roles import RoleConstants
from shared.database.models import User
from services.auth.app.core.security import verify_password, get_password_hash, create_access_token
from services.auth.app.models.schemas import UserCreate, UserUpdate, Token, UserResponse
from shared.config.settings import settings

class AuthService:
    
    @staticmethod
    async def create_user(db: Session, user_data: UserCreate) -> User:
        if db.query(User).filter(User.user_email == user_data.user_email).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Validar el role_id si se proporciona
        if user_data.role_id is not None and not RoleConstants.is_valid_role(user_data.role_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid role_id"
            )

        hashed_password = get_password_hash(user_data.password)
        db_user = User(
            user_name=user_data.user_name,
            user_last_name=user_data.user_last_name,
            user_email=user_data.user_email,
            user_city=user_data.user_city,
            user_country=user_data.user_country,
            user_number=user_data.user_number,
            user_bio=user_data.user_bio,
            password=hashed_password,
            role_id=user_data.role_id,  # Será null por defecto si no se especifica
            status=True
        )
        
        try:
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            return db_user
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating user: {str(e)}"
            )

    @staticmethod
    async def is_admin(user: User) -> bool:
        """Verifica si el usuario tiene rol administrativo"""
        return user.role_id in [RoleConstants.ADMIN, RoleConstants.SUPER_ADMIN]
        
    @staticmethod
    async def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
        user = db.query(User).filter(User.user_email == email).first()
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        return user

    @staticmethod
    async def create_token(user: User) -> Token:
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            subject=str(user.user_id),
            expires_delta=access_token_expires
        )

        # Crear el UserResponse manualmente para asegurar que todos los campos estén presentes
        user_response = {
            "user_id": user.user_id,
            "user_name": user.user_name,
            "user_last_name": user.user_last_name,
            "user_email": user.user_email,
            "user_city": user.user_city,
            "user_country": user.user_country,
            "user_number": user.user_number,
            "user_bio": user.user_bio,
            "profile_picture": user.profile_picture,
            "status": user.status,
            "role_id": user.role_id  # Asegurarte de que este campo exista
        }

        return Token(
            access_token=access_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user=UserResponse(**user_response)
        )

    @staticmethod
    @staticmethod
    async def update_user(db: Session, current_user: User, user_data: UserUpdate) -> User:
        """
        Actualiza los datos del usuario
        """
        # Si se está actualizando el email, verificar que no exista
        if user_data.user_email and user_data.user_email != current_user.user_email:
            if db.query(User).filter(User.user_email == user_data.user_email).first():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )

        # Actualizar los campos
        for field, value in user_data.dict(exclude_unset=True).items():
            if value is not None:  # Solo actualizar si el valor no es None
                setattr(current_user, field, value)

        try:
            current_user.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(current_user)
            return current_user
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error updating user: {str(e)}"
            )

    @staticmethod
    async def change_password(db: Session, user: User, current_password: str, new_password: str) -> bool:
        if not verify_password(current_password, user.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect password"
            )
        
        user.password = get_password_hash(new_password)
        try:
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error changing password"
            )