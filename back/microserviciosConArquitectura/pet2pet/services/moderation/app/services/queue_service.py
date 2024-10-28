# services/moderation/app/services/queue_service.py
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from typing import List, Dict, Optional
from shared.database.models import Report, ModerationAction, User
from services.moderation.app.models.schemas import ContentType, ContentStatus, ReportResponse
import asyncio
from collections import deque

class ModerationQueue:
    def __init__(self):
        self.high_priority = deque()  # Para contenido urgente
        self.medium_priority = deque()  # Para contenido regular
        self.low_priority = deque()  # Para revisiones rutinarias
        self.processing = set()  # Contenido actualmente en revisión
        self.max_processing = 100  # Máximo de items en procesamiento simultáneo

class QueueService:
    def __init__(self):
        self.queue = ModerationQueue()
        self.priority_thresholds = {
            "high": 0.8,    # Contenido con alta probabilidad de ser dañino
            "medium": 0.5,  # Contenido con probabilidad media
            "low": 0.2      # Contenido con baja probabilidad
        }

    async def add_to_queue(
        self,
        db: Session,
        content_id: int,
        content_type: ContentType,
        priority_score: float,
        reporter_trust_score: float,
        additional_context: Dict = None
    ) -> bool:
        """
        Añade contenido a la cola de moderación con prioridad apropiada
        """
        if content_id in self.queue.processing:
            return False

        queue_item = {
            "content_id": content_id,
            "content_type": content_type,
            "priority_score": priority_score,
            "reporter_trust_score": reporter_trust_score,
            "timestamp": datetime.now(timezone.utc),
            "context": additional_context or {},
            "attempts": 0
        }

        # Determinar la cola basada en prioridad
        if priority_score >= self.priority_thresholds["high"]:
            self.queue.high_priority.append(queue_item)
        elif priority_score >= self.priority_thresholds["medium"]:
            self.queue.medium_priority.append(queue_item)
        else:
            self.queue.low_priority.append(queue_item)

        # Actualizar estado en la base de datos
        report = db.query(Report).filter(
            Report.reported_content_id == content_id
        ).first()
        
        if report:
            report.status = ContentStatus.UNDER_REVIEW
            db.commit()

        return True

    async def get_next_item(self, db: Session) -> Optional[Dict]:
        """
        Obtiene el siguiente item a moderar basado en prioridad
        """
        if len(self.queue.processing) >= self.queue.max_processing:
            return None

        # Revisar colas en orden de prioridad
        for priority_queue in [
            self.queue.high_priority,
            self.queue.medium_priority,
            self.queue.low_priority
        ]:
            while priority_queue:
                item = priority_queue.popleft()
                if item["content_id"] not in self.queue.processing:
                    self.queue.processing.add(item["content_id"])
                    return item

        return None

    async def process_queue(self, db: Session):
        """
        Procesa la cola de moderación de manera continua
        """
        while True:
            item = await self.get_next_item(db)
            if not item:
                await asyncio.sleep(1)  # Esperar si no hay items
                continue

            try:
                # Procesar el item
                await self.handle_queue_item(db, item)
            except Exception as e:
                # Manejar error y posiblemente reintentar
                if item["attempts"] < 3:  # Máximo 3 intentos
                    item["attempts"] += 1
                    await self.add_to_queue(
                        db,
                        item["content_id"],
                        item["content_type"],
                        item["priority_score"],
                        item["reporter_trust_score"],
                        item["context"]
                    )
            finally:
                self.queue.processing.remove(item["content_id"])

    async def handle_queue_item(self, db: Session, item: Dict):
        """
        Procesa un item específico de la cola
        """
        # Actualizar estado
        report = db.query(Report).filter(
            Report.reported_content_id == item["content_id"]
        ).first()
        
        if not report:
            return

        # Verificar contenido basado en tipo
        if item["content_type"] == ContentType.POST:
            await self.handle_post_moderation(db, item)
        elif item["content_type"] == ContentType.COMMENT:
            await self.handle_comment_moderation(db, item)
        elif item["content_type"] == ContentType.PROFILE:
            await self.handle_profile_moderation(db, item)

    async def handle_post_moderation(self, db: Session, item: Dict):
        """
        Maneja la moderación específica de posts
        """
        # Implementar lógica específica para posts
        pass

    async def handle_comment_moderation(self, db: Session, item: Dict):
        """
        Maneja la moderación específica de comentarios
        """
        # Implementar lógica específica para comentarios
        pass

    async def handle_profile_moderation(self, db: Session, item: Dict):
        """
        Maneja la moderación específica de perfiles
        """
        # Implementar lógica específica para perfiles
        pass

    async def get_queue_stats(self) -> Dict:
        """
        Obtiene estadísticas actuales de la cola
        """
        return {
            "high_priority_count": len(self.queue.high_priority),
            "medium_priority_count": len(self.queue.medium_priority),
            "low_priority_count": len(self.queue.low_priority),
            "currently_processing": len(self.queue.processing)
        }