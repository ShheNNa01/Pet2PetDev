import asyncio
import json
from typing import Any
from sqlalchemy.orm import Session
from shared.database.session import SessionLocal
from services.notifications.app.core.event_broker import event_broker
from services.notifications.app.services.notification_service import NotificationService
from services.notifications.app.models.schemas import NotificationCreate, NotificationType

class NotificationWorker:
    def __init__(self):
        self.event_broker = event_broker
        self.running = False

    async def process_event(self, event_data: dict[str, Any], db: Session):
        """Procesa un evento y crea la notificación correspondiente"""
        try:
            notification_data = NotificationCreate(
                user_id=event_data['user_id'],
                type=NotificationType(event_data['type']),
                related_id=event_data.get('related_id'),
                message=event_data.get('message')
            )
            await NotificationService.create_notification(db, notification_data)
        except Exception as e:
            print(f"Error processing notification event: {str(e)}")

    async def start(self):
        """Inicia el worker"""
        self.running = True
        await self.event_broker.connect()
        pubsub = await self.event_broker.subscribe('notifications')
        
        while self.running:
            try:
                message = await pubsub.get_message(ignore_subscribe_messages=True)
                if message:
                    event_data = json.loads(message['data'])
                    db = SessionLocal()
                    try:
                        await self.process_event(event_data, db)
                    finally:
                        db.close()
            except Exception as e:
                print(f"Error in notification worker: {str(e)}")
            await asyncio.sleep(0.1)

    async def stop(self):
        """Detiene el worker"""
        self.running = False

notification_worker = NotificationWorker()