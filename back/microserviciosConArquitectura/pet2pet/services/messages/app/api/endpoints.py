from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from shared.database.session import get_db
from shared.database.models import User, Pet, PrivateMessage
from services.messages.app.models.schemas import (
    MessageCreate,
    MessageResponse,
    MessageUpdate,
    ConversationResponse,
    UnreadCountResponse
)
from services.messages.app.services.message_service import MessageService
from services.auth.app.api.dependencies import get_current_active_user

router = APIRouter()

@router.post("/", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def send_message(
    message: MessageCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Enviar un mensaje a otra mascota.
    
    Args:
        message: Datos del mensaje a enviar
        current_user: Usuario autenticado actual
        db: Sesión de base de datos
    
    Returns:
        MessageResponse: Mensaje creado
        
    Raises:
        HTTPException: Si el usuario no tiene una mascota o si hay error al enviar
    """
    # Verificar que el usuario tiene una mascota
    sender_pet = db.query(Pet).filter(
        Pet.user_id == current_user.user_id,
        Pet.status == True
    ).first()
    
    if not sender_pet:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User doesn't have an active pet"
        )

    return await MessageService.create_message(db, sender_pet.pet_id, message)

@router.get("/conversations", response_model=List[ConversationResponse])
async def get_conversations(
    skip: int = Query(0, ge=0, description="Número de conversaciones a saltar"),
    limit: int = Query(20, ge=1, le=50, description="Número máximo de conversaciones a retornar"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Obtener todas las conversaciones del usuario.
    
    Returns:
        List[ConversationResponse]: Lista de conversaciones con el último mensaje
    """
    # Verificar que el usuario tiene una mascota
    sender_pet = db.query(Pet).filter(
        Pet.user_id == current_user.user_id,
        Pet.status == True
    ).first()
    
    if not sender_pet:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User doesn't have an active pet"
        )

    return await MessageService.get_conversations(
        db, 
        sender_pet.pet_id,
        skip=skip,
        limit=limit
    )

@router.get("/conversation/{other_pet_id}", response_model=List[MessageResponse])
async def get_conversation(
    other_pet_id: int,
    skip: int = Query(0, ge=0, description="Número de mensajes a saltar"),
    limit: int = Query(50, ge=1, le=100, description="Número máximo de mensajes a retornar"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Obtener mensajes de una conversación específica con otra mascota.
    
    Args:
        other_pet_id: ID de la mascota con la que se tiene la conversación
        skip: Número de mensajes a saltar para paginación
        limit: Número máximo de mensajes a retornar
    
    Returns:
        List[MessageResponse]: Lista de mensajes de la conversación
    """
    # Verificar que el usuario tiene una mascota
    sender_pet = db.query(Pet).filter(
        Pet.user_id == current_user.user_id,
        Pet.status == True
    ).first()
    
    if not sender_pet:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User doesn't have an active pet"
        )

    # Verificar que la otra mascota existe
    other_pet = db.query(Pet).filter(
        Pet.pet_id == other_pet_id,
        Pet.status == True
    ).first()
    
    if not other_pet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Other pet not found or not active"
        )

    # Marcar mensajes como leídos automáticamente
    await MessageService.mark_as_read(db, sender_pet.pet_id, other_pet_id)
    
    return await MessageService.get_messages(
        db, 
        sender_pet.pet_id, 
        other_pet_id, 
        skip, 
        limit
    )

@router.put("/conversation/{other_pet_id}/read", status_code=status.HTTP_200_OK)
async def mark_conversation_as_read(
    other_pet_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Marcar todos los mensajes de una conversación como leídos.
    """
    # Verificar que el usuario tiene una mascota
    sender_pet = db.query(Pet).filter(
        Pet.user_id == current_user.user_id,
        Pet.status == True
    ).first()
    
    if not sender_pet:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User doesn't have an active pet"
        )

    await MessageService.mark_as_read(db, sender_pet.pet_id, other_pet_id)
    return {
        "status": "success",
        "message": "All messages in conversation marked as read",
        "timestamp": datetime.utcnow()
    }

@router.get("/unread/count", response_model=UnreadCountResponse)
async def get_unread_count(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Obtener el número total de mensajes no leídos y estadísticas.
    
    Returns:
        UnreadCountResponse: Conteo de mensajes no leídos y estadísticas adicionales
    """
    # Verificar que el usuario tiene una mascota
    sender_pet = db.query(Pet).filter(
        Pet.user_id == current_user.user_id,
        Pet.status == True
    ).first()
    
    if not sender_pet:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User doesn't have an active pet"
        )

    return await MessageService.get_unread_stats(db, sender_pet.pet_id)

@router.delete("/conversation/{other_pet_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_conversation(
    other_pet_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Eliminar toda la conversación con otra mascota.
    """
    # Verificar que el usuario tiene una mascota
    sender_pet = db.query(Pet).filter(
        Pet.user_id == current_user.user_id,
        Pet.status == True
    ).first()
    
    if not sender_pet:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User doesn't have an active pet"
        )

    await MessageService.delete_conversation(db, sender_pet.pet_id, other_pet_id)

@router.get("/search", response_model=List[MessageResponse])
async def search_messages(
    query: str = Query(..., min_length=3, description="Texto a buscar en los mensajes"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=50),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Buscar mensajes que contengan el texto especificado.
    """
    # Verificar que el usuario tiene una mascota
    sender_pet = db.query(Pet).filter(
        Pet.user_id == current_user.user_id,
        Pet.status == True
    ).first()
    
    if not sender_pet:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User doesn't have an active pet"
        )

    return await MessageService.search_messages(
        db,
        sender_pet.pet_id,
        query,
        skip,
        limit
    )