# services/moderation/app/services/report_service.py
from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import List, Dict, Optional, Tuple
from shared.database.models import Report, User, ModerationAction, Notification
from services.moderation.app.models.schemas import (
    ReportCreate, ContentType, ContentStatus,
    ReportResponse, UserModerationProfile
)

class ReportService:
    async def create_report(
        self,
        db: Session,
        report_data: ReportCreate,
        reporter_id: int
    ) -> Report:
        """
        Crea un nuevo reporte y maneja la lógica inicial de procesamiento
        """
        # Verificar si ya existe un reporte similar
        existing_report = db.query(Report).filter(
            Report.reported_content_id == report_data.reported_content_id,
            Report.content_type == report_data.content_type,
            Report.status == ContentStatus.PENDING
        ).first()

        if existing_report:
            # Actualizar reporte existente con nueva información
            existing_report.reason = report_data.reason
            existing_report.description = report_data.description or existing_report.description
            db.commit()
            return existing_report

        # Crear nuevo reporte
        new_report = Report(
            reported_by_user_id=reporter_id,
            reported_content_id=report_data.reported_content_id,
            content_type=report_data.content_type,
            reason=report_data.reason,
            description=report_data.description,
            evidence=report_data.evidence,
            status=ContentStatus.PENDING,
            created_at=datetime.now(timezone.utc)
        )

        db.add(new_report)
        db.commit()
        db.refresh(new_report)

        # Notificar a moderadores
        await self.notify_moderators(db, new_report)

        return new_report

    async def get_report_details(
        self,
        db: Session,
        report_id: int
    ) -> Optional[Report]:
        """
        Obtiene detalles completos de un reporte
        """
        return db.query(Report).filter(Report.report_id == report_id).first()

    async def update_report_status(
        self,
        db: Session,
        report_id: int,
        new_status: ContentStatus,
        moderator_id: int,
        notes: str = None
    ) -> Tuple[Report, bool]:
        """
        Actualiza el estado de un reporte y realiza acciones necesarias
        """
        report = await self.get_report_details(db, report_id)
        if not report:
            return None, False

        report.status = new_status
        report.updated_at = datetime.now(timezone.utc)

        # Registrar acción de moderación
        action = ModerationAction(
            content_id=report.reported_content_id,
            content_type=report.content_type,
            action=f"report_{new_status.value}",
            reason=report.reason,
            moderated_by=moderator_id,
            notes=notes
        )
        
        db.add(action)

        # Notificar al reportador
        notification = Notification(
            user_id=report.reported_by_user_id,
            type="report_status_update",
            related_id=report_id,
            message=f"El estado de tu reporte ha sido actualizado a: {new_status.value}",
            additional_data={
                "new_status": new_status.value,
                "content_type": report.content_type
            }
        )
        
        db.add(notification)
        db.commit()

        return report, True

    async def get_user_report_history(
        self,
        db: Session,
        user_id: int,
        as_reporter: bool = True
    ) -> List[Report]:
        """
        Obtiene el historial de reportes de un usuario
        """
        if as_reporter:
            return db.query(Report).filter(
                Report.reported_by_user_id == user_id
            ).order_by(Report.created_at.desc()).all()
        else:
            return db.query(Report).filter(
                Report.reported_content_id == user_id,
                Report.content_type == ContentType.PROFILE
            ).order_by(Report.created_at.desc()).all()

    async def get_pending_reports(
        self,
        db: Session,
        content_type: Optional[ContentType] = None,
        priority: bool = False
    ) -> List[Report]:
        """
        Obtiene reportes pendientes, opcionalmente filtrados y priorizados
        """
        query = db.query(Report).filter(Report.status == ContentStatus.PENDING)
        
        if content_type:
            query = query.filter(Report.content_type == content_type)

        if priority:
            # Priorizar basado en cantidad de reportes similares y severidad
            query = query.join(User, Report.reported_by_user_id == User.user_id)
            query = query.order_by(
                func.count(Report.reported_content_id).desc(),
                Report.created_at.asc()
            )
            query = query.group_by(Report.report_id, User.user_id)

        return query.all()

    async def get_report_statistics(
        self,
        db: Session,
        time_range: timedelta = timedelta(days=30)
    ) -> Dict:
        """
        Obtiene estadísticas de reportes para un período de tiempo
        """
        start_date = datetime.now(timezone.utc) - time_range
        
        # Consultas base
        base_query = db.query(Report).filter(Report.created_at >= start_date)
        
        # Total de reportes
        total_reports = base_query.count()
        
        # Reportes por estado
        reports_by_status = (
            base_query
            .with_entities(Report.status, func.count(Report.report_id))
            .group_by(Report.status)
            .all()
        )
        
        # Reportes por tipo de contenido
        reports_by_type = (
            base_query
            .with_entities(Report.content_type, func.count(Report.report_id))
            .group_by(Report.content_type)
            .all()
        )
        
        # Reportes por razón
        reports_by_reason = (
            base_query
            .with_entities(Report.reason, func.count(Report.report_id))
            .group_by(Report.reason)
            .all()
        )

        return {
            "total_reports": total_reports,
            "by_status": {status: count for status, count in reports_by_status},
            "by_type": {type_: count for type_, count in reports_by_type},
            "by_reason": {reason: count for reason, count in reports_by_reason},
            "time_range_days": time_range.days
        }

    async def notify_moderators(self, db: Session, report: Report):
        """
        Notifica a los moderadores sobre un nuevo reporte
        """
        # Obtener moderadores
        moderators = db.query(User).filter(
            User.role_id.in_([1, 2])  # IDs de roles de moderador y admin
        ).all()

        # Crear notificaciones
        for moderator in moderators:
            notification = Notification(
                user_id=moderator.user_id,
                type="new_report",
                related_id=report.report_id,
                message=f"Nuevo reporte de {report.content_type}: {report.reason}",
                additional_data={
                    "content_type": report.content_type,
                    "reason": report.reason,
                    "reporter_id": report.reported_by_user_id
                }
            )
            db.add(notification)

        db.commit()