from typing import Generator
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from shared.database.session import get_db
from shared.database.models import User
from services.auth.app.api.dependencies import get_current_active_user

async def get_notification_db(db: Session = Depends(get_db)) -> Generator: # type: ignore
    try:
        yield db
    finally:
        db.close()

async def check_notification_access(
    user: User = Depends(get_current_active_user),
    db: Session = Depends(get_notification_db)
) -> User:
    """
    Verificar que el usuario tiene acceso a las notificaciones
    Se puede expandir con lógica adicional si es necesario
    """
    if not user.status:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user cannot access notifications"
        )
    return user