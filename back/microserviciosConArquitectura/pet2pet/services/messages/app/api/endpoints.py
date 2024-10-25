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
    ConversationResponse
)
from services.messages.app.services.message_service import MessageService
from services.auth.app.api.dependencies import get_current_active_user

router = APIRouter()

@router.post("", response_model=MessageResponse)
async def send_message(
    message: MessageCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Enviar un mensaje a otra mascota
    """
    # Verificar que el usuario tiene una mascota
    sender_pet = db.query(Pet).filter(Pet.user_id == current_user.user_id).first()
    if not sender_pet:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User doesn't have a pet"
        )

    return await MessageService.create_message(db, sender_pet.pet_id, message)

@router.get("/conversations", response_model=List[ConversationResponse])
async def get_conversations(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Obtener todas las conversaciones del usuario
    """
    # Verificar que el usuario tiene una mascota
    sender_pet = db.query(Pet).filter(Pet.user_id == current_user.user_id).first()
    if not sender_pet:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User doesn't have a pet"
        )

    return await MessageService.get_conversations(db, sender_pet.pet_id)

@router.get("/{other_pet_id}", response_model=List[MessageResponse])
async def get_conversation(
    other_pet_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Obtener mensajes de una conversación específica
    """
    # Verificar que el usuario tiene una mascota
    sender_pet = db.query(Pet).filter(Pet.user_id == current_user.user_id).first()
    if not sender_pet:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User doesn't have a pet"
        )

    # Marcar mensajes como leídos
    await MessageService.mark_as_read(db, sender_pet.pet_id, other_pet_id)
    
    return await MessageService.get_messages(
        db, 
        sender_pet.pet_id, 
        other_pet_id, 
        skip, 
        limit
    )

@router.put("/{other_pet_id}/read", status_code=status.HTTP_200_OK)
async def mark_conversation_as_read(
    other_pet_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Marcar todos los mensajes de una conversación como leídos
    """
    # Verificar que el usuario tiene una mascota
    sender_pet = db.query(Pet).filter(Pet.user_id == current_user.user_id).first()
    if not sender_pet:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User doesn't have a pet"
        )

    await MessageService.mark_as_read(db, sender_pet.pet_id, other_pet_id)
    return {"status": "Messages marked as read"}

@router.get("/unread/count", response_model=dict)
async def get_unread_count(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Obtener el número total de mensajes no leídos
    """
    # Verificar que el usuario tiene una mascota
    sender_pet = db.query(Pet).filter(Pet.user_id == current_user.user_id).first()
    if not sender_pet:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User doesn't have a pet"
        )

    unread_count = db.query(PrivateMessage).filter(
        PrivateMessage.receiver_pet_id == sender_pet.pet_id,
        PrivateMessage.read_status == False
    ).count()

    return {"unread_count": unread_count}