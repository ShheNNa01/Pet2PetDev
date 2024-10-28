# services/moderation/app/services/moderation_service.py
from datetime import datetime, timezone
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List, Dict, Optional, Tuple
from shared.database.models import Report, User, Notification
from services.moderation.app.models.schemas import (
    ModerationStats, ReportCreate, ReportUpdate, ContentType, ContentStatus,
    AutoModResult, ContentReview, ModerationAction, UserModerationProfile
)
from ..core.content_rules import ContentRules

class ModerationService:
    def __init__(self):
        self.content_rules = ContentRules()

    async def create_report(
        self,
        db: Session,
        report_data: ReportCreate,
        reported_by_user_id: int
    ) -> Report:
        """Crea un nuevo reporte de contenido"""
        db_report = Report(
            reported_by_user_id=reported_by_user_id,
            reported_content_id=report_data.reported_content_id,
            content_type=report_data.content_type,
            reason=report_data.reason,
            description=report_data.description,
            evidence=report_data.evidence,
            status=ContentStatus.PENDING
        )
        
        db.add(db_report)
        db.commit()
        db.refresh(db_report)
        
        # Crear notificación para moderadores
        notification = Notification(
            user_id=None,  # Se enviará a todos los moderadores
            type="new_report",
            related_id=db_report.report_id,
            message=f"Nuevo reporte de contenido: {report_data.reason}",
            additional_data={
                "content_type": report_data.content_type,
                "reason": report_data.reason
            }
        )
        db.add(notification)
        db.commit()
        
        return db_report

    async def review_content(
        self,
        db: Session,
        content_review: ContentReview
    ) -> AutoModResult:
        """Revisa automáticamente el contenido usando las reglas establecidas"""
        sensitivity_scores = self.content_rules.get_content_sensitivity(
            str(content_review.content_data),
            content_review.filter_settings.sensitivity_level if content_review.filter_settings else 3
        )
        
        flags = []
        for category, score in sensitivity_scores.items():
            if score > 0.7:  # Umbral de detección
                flags.append(category)
        
        is_approved = len(flags) == 0
        confidence_score = 1.0 - max(sensitivity_scores.values(), default=0.0)
        
        recommendation = ContentStatus.APPROVED if is_approved else ContentStatus.FLAGGED
        
        return AutoModResult(
            is_approved=is_approved,
            confidence_score=confidence_score,
            flags=flags,
            detected_issues=sensitivity_scores,
            recommendation=recommendation
        )

    async def take_moderation_action(
        self,
        db: Session,
        action: ModerationAction
    ) -> Tuple[bool, str]:
        """Ejecuta una acción de moderación"""
        try:
            # Registrar la acción
            # Aquí implementarías la lógica específica según el tipo de contenido
            
            # Notificar al usuario afectado
            notification = Notification(
                user_id=action.moderated_by,  # ID del usuario afectado
                type="moderation_action",
                related_id=action.content_id,
                message=f"Acción de moderación: {action.action}",
                additional_data={
                    "action": action.action,
                    "reason": action.reason,
                    "duration": action.duration
                }
            )
            db.add(notification)
            db.commit()
            
            return True, "Acción de moderación ejecutada correctamente"
        except Exception as e:
            db.rollback()
            return False, str(e)

    async def get_user_moderation_profile(
        self,
        db: Session,
        user_id: int
    ) -> UserModerationProfile:
        """Obtiene el perfil de moderación de un usuario"""
        # Obtener estadísticas de reportes
        reports_received = db.query(Report).filter(
            Report.reported_content_id == user_id,
            Report.content_type == ContentType.PROFILE
        ).all()
        
        reports_made = db.query(Report).filter(
            Report.reported_by_user_id == user_id
        ).all()
        
        # Calcular estadísticas
        warning_count = db.query(ModerationAction).filter(
            ModerationAction.content_id == user_id,
            ModerationAction.action == "warning"
        ).count()
        
        ban_count = db.query(ModerationAction).filter(
            ModerationAction.content_id == user_id,
            ModerationAction.action == "temporary_ban"
        ).count()
        
        # Obtener últimas acciones
        last_warning = db.query(ModerationAction).filter(
            ModerationAction.content_id == user_id,
            ModerationAction.action == "warning"
        ).order_by(ModerationAction.created_at.desc()).first()
        
        last_ban = db.query(ModerationAction).filter(
            ModerationAction.content_id == user_id,
            ModerationAction.action == "temporary_ban"
        ).order_by(ModerationAction.created_at.desc()).first()
        
        # Obtener historial completo
        history = db.query(ModerationAction).filter(
            ModerationAction.content_id == user_id
        ).order_by(ModerationAction.created_at.desc()).all()
        
        # Calcular trust score
        user = db.query(User).filter(User.user_id == user_id).first()
        account_age_days = (datetime.now(timezone.utc) - user.created_at).days
        
        trust_score = self.content_rules.calculate_trust_score(
            total_posts=len(reports_made),
            reports_received=len(reports_received),
            reports_confirmed=len([r for r in reports_received if r.status == ContentStatus.APPROVED]),
            account_age_days=account_age_days
        )
        
        return UserModerationProfile(
            user_id=user_id,
            total_reports_received=len(reports_received),
            total_reports_made=len(reports_made),
            warning_count=warning_count,
            temporary_ban_count=ban_count,
            last_warning_date=last_warning.created_at if last_warning else None,
            last_ban_date=last_ban.created_at if last_ban else None,
            current_status="active" if trust_score > 50 else "restricted",
            trust_score=trust_score,
            moderation_history=[{
                "action": action.action,
                "reason": action.reason,
                "date": action.created_at,
                "duration": action.duration,
                "notes": action.notes
            } for action in history]
        )

    async def get_moderation_stats(self, db: Session) -> ModerationStats:
        """Obtiene estadísticas generales de moderación"""
        total_reports = db.query(Report).count()
        pending_reports = db.query(Report).filter(Report.status == ContentStatus.PENDING).count()
        resolved_reports = total_reports - pending_reports
        
        # Contar acciones automatizadas vs manuales
        automated_actions = db.query(ModerationAction).filter(
            ModerationAction.moderated_by == None
        ).count()
        
        manual_actions = db.query(ModerationAction).filter(
            ModerationAction.moderated_by != None
        ).count()
        
        # Calcular tiempo promedio de respuesta
        resolved_reports = db.query(Report).filter(
            Report.status.in_([ContentStatus.APPROVED, ContentStatus.REJECTED])
        ).all()
        
        total_response_time = sum(
            (report.updated_at - report.created_at).total_seconds() / 3600
            for report in resolved_reports
            if report.updated_at
        )
        
        avg_response_time = (
            total_response_time / len(resolved_reports)
            if resolved_reports else 0
        )
        
        # Contar razones comunes
        reason_counts = {}
        for report in db.query(Report).all():
            reason_counts[report.reason] = reason_counts.get(report.reason, 0) + 1
        
        # Estadísticas diarias
        today = datetime.now(timezone.utc).date()
        daily_reports = db.query(Report).filter(
            func.date(Report.created_at) == today
        ).count()
        
        daily_actions = db.query(ModerationAction).filter(
            func.date(ModerationAction.created_at) == today
        ).count()
        
        return ModerationStats(
            total_reports=total_reports,
            pending_reports=pending_reports,
            resolved_reports=resolved_reports,
            automated_actions=automated_actions,
            manual_actions=manual_actions,
            average_response_time=avg_response_time,
            common_reasons=reason_counts,
            daily_stats={
                "reports": daily_reports,
                "actions": daily_actions
            }
        )