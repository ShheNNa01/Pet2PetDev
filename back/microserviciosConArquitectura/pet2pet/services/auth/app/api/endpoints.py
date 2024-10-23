# services/auth/app/api/endpoints.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Any

from services.auth.app.models.schemas import (
    UserCreate, UserResponse, Token, UserUpdate,
    ChangePasswordRequest, RequestPasswordReset, ResetPassword
)
from services.auth.app.services.auth_service import AuthService
from services.auth.app.api.dependencies import get_current_active_user, get_auth_service
from shared.database.session import get_db
from shared.database.models import User

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    auth_service: AuthService = Depends(get_auth_service)
) -> Any:
    return await auth_service.create_user(db, user_data)

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
    auth_service: AuthService = Depends(get_auth_service)
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    user = await auth_service.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return await auth_service.create_token(user)

@router.get("/me", response_model=UserResponse)
async def read_users_me(
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Get current user.
    """
    return current_user

@router.put("/me", response_model=UserResponse)
async def update_user_me(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
    auth_service: AuthService = Depends(get_auth_service)
) -> Any:
    """
    Update current user.
    """
    return await auth_service.update_user(db, current_user, user_data)

@router.post("/change-password", response_model=dict)
async def change_password(
    password_data: ChangePasswordRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
    auth_service: AuthService = Depends(get_auth_service)
) -> Any:
    """
    Change current user password.
    """
    success = await auth_service.change_password(
        db, 
        current_user, 
        password_data.current_password, 
        password_data.new_password
    )
    return {"message": "Password changed successfully"}

@router.post("/password-reset-request", response_model=dict)
async def request_password_reset(
    request_data: RequestPasswordReset,
    db: Session = Depends(get_db),
    auth_service: AuthService = Depends(get_auth_service)
) -> Any:
    """
    Request a password reset.
    """
    # Implementar lógica de reset de contraseña
    return {"message": "If the email exists, a password reset link will be sent"}

@router.post("/reset-password", response_model=dict)
async def reset_password(
    reset_data: ResetPassword,
    db: Session = Depends(get_db),
    auth_service: AuthService = Depends(get_auth_service)
) -> Any:
    """
    Reset password with token.
    """
    # Implementar lógica de reset de contraseña
    return {"message": "Password reset successfully"}