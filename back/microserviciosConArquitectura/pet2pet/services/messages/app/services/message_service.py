from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import case, func, or_, desc, asc, and_

from datetime import datetime
from typing import List, Optional

from shared.database.models import PrivateMessage, Pet
from services.messages.app.models.schemas import MessageCreate, MessageUpdate

class MessageService:
    @staticmethod
    async def create_message(
        db: Session, 
        sender_pet_id: int, 
        message_data: MessageCreate
    ) -> PrivateMessage:
        # Verificar que el receptor existe
        receiver_pet = db.query(Pet).filter(Pet.pet_id == message_data.receiver_pet_id).first()
        if not receiver_pet:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Receiver pet not found"
            )
            
        # Crear el mensaje
        db_message = PrivateMessage(
            sender_pet_id=sender_pet_id,
            receiver_pet_id=message_data.receiver_pet_id,
            message=message_data.message,
            read_status=False
        )

        try:
            db.add(db_message)
            db.commit()
            db.refresh(db_message)
            return db_message
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Could not create message: {str(e)}"
            )

    @staticmethod
    async def get_conversations(db: Session, pet_id: int) -> List[dict]:
        try:
            # Obtener las últimas conversaciones
            latest_messages = (
                db.query(
                    PrivateMessage.sender_pet_id,
                    PrivateMessage.receiver_pet_id,
                    func.max(PrivateMessage.created_at).label('max_date')
                )
                .filter(
                    or_(
                        PrivateMessage.sender_pet_id == pet_id,
                        PrivateMessage.receiver_pet_id == pet_id
                    )
                )
                .group_by(
                    PrivateMessage.sender_pet_id,
                    PrivateMessage.receiver_pet_id
                )
                .subquery('latest_messages')
            )

            # Obtener los detalles completos de las conversaciones
            conversations_query = (
                db.query(
                    Pet,
                    PrivateMessage,
                    func.count(
                        case(
                            (and_(
                                PrivateMessage.read_status == False,
                                PrivateMessage.receiver_pet_id == pet_id
                            ), 1)
                        )
                    ).label('unread_count')
                )
                .join(
                    latest_messages,
                    or_(
                        and_(
                            Pet.pet_id == latest_messages.c.sender_pet_id,
                            Pet.pet_id != pet_id
                        ),
                        and_(
                            Pet.pet_id == latest_messages.c.receiver_pet_id,
                            Pet.pet_id != pet_id
                        )
                    )
                )
                .join(
                    PrivateMessage,
                    and_(
                        PrivateMessage.created_at == latest_messages.c.max_date,
                        or_(
                            and_(
                                PrivateMessage.sender_pet_id == latest_messages.c.sender_pet_id,
                                PrivateMessage.receiver_pet_id == latest_messages.c.receiver_pet_id
                            ),
                            and_(
                                PrivateMessage.sender_pet_id == latest_messages.c.receiver_pet_id,
                                PrivateMessage.receiver_pet_id == latest_messages.c.sender_pet_id
                            )
                        )
                    )
                )
                .group_by(Pet.pet_id, PrivateMessage.message_id)
                .order_by(PrivateMessage.created_at.desc())
            )

            conversations = []
            for pet, message, unread_count in conversations_query.all():
                conversations.append({
                    "pet_id": pet.pet_id,
                    "pet_name": pet.name,
                    "pet_picture": pet.pet_picture,
                    "last_message": message.message,
                    "last_message_time": message.created_at,
                    "unread_count": unread_count
                })

            return conversations

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error getting conversations: {str(e)}"
            )

    @staticmethod
    async def get_messages(
        db: Session,
        pet_id: int,
        other_pet_id: int,
        skip: int = 0,
        limit: int = 50
    ) -> List[PrivateMessage]:
        return db.query(PrivateMessage).filter(
            or_(
                and_(
                    PrivateMessage.sender_pet_id == pet_id,
                    PrivateMessage.receiver_pet_id == other_pet_id
                ),
                and_(
                    PrivateMessage.sender_pet_id == other_pet_id,
                    PrivateMessage.receiver_pet_id == pet_id
                )
            )
        ).order_by(
            PrivateMessage.created_at.desc()
        ).offset(skip).limit(limit).all()

    @staticmethod
    async def mark_as_read(
        db: Session,
        pet_id: int,
        other_pet_id: int
    ) -> None:
        try:
            db.query(PrivateMessage).filter(
                PrivateMessage.sender_pet_id == other_pet_id,
                PrivateMessage.receiver_pet_id == pet_id,
                PrivateMessage.read_status == False
            ).update(
                {"read_status": True}
            )
            db.commit()
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Could not mark messages as read: {str(e)}"
            )