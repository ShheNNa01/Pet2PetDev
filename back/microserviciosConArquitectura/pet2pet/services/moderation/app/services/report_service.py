from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import logging

from shared.database.models import Report, User, Post, Comment, Group, GroupPost
from ..models.schemas import (
    ReportCreate,
    ReportResponse,
    ModerationStatus,
    ModerationAction,
    ContentType
)

logger = logging.getLogger(__name__)

class ReportService:
    @staticmethod
    async def create_report(
        db: Session,
        report_data: ReportCreate,
        reporter_id: int
    ) -> Report:
        """
        Crear un nuevo reporte
        """
        try:
            # Verificar si el contenido existe
            if not await ReportService._verify_content_exists(
                db,
                report_data.content_type,
                report_data.content_id
            ):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Reported content not found"
                )

            # Verificar si ya existe un reporte similar
            existing_report = db.query(Report).filter(
                Report.content_type == report_data.content_type,
                Report.content_id == report_data.content_id,
                Report.reporter_id == reporter_id,
                Report.status.in_([
                    ModerationStatus.PENDING,
                    ModerationStatus.UNDER_REVIEW
                ])
            ).first()

            if existing_report:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="You have already reported this content"
                )

            # Crear el reporte
            report = Report(
                content_type=report_data.content_type,
                content_id=report_data.content_id,
                reporter_id=reporter_id,
                reason=report_data.reason,
                description=report_data.description,
                evidence_urls=report_data.evidence_urls,
                status=ModerationStatus.PENDING,
                created_at=datetime.utcnow()
            )

            db.add(report)
            db.commit()
            db.refresh(report)

            # Verificar si se necesita auto-moderación
            await ReportService._check_for_auto_moderation(db, report)

            return report

        except HTTPException:
            db.rollback()
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating report: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating report: {str(e)}"
            )

    @staticmethod
    async def get_report(
        db: Session,
        report_id: int,
        user_id: int
    ) -> Report:
        """
        Obtener un reporte específico
        """
        report = db.query(Report).filter(Report.report_id == report_id).first()
        
        if not report:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Report not found"
            )

        # Verificar permisos (solo el reportador o moderadores)
        if report.reporter_id != user_id and not await ReportService._is_moderator(db, user_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to view this report"
            )

        return report

    @staticmethod
    async def get_reports(
        db: Session,
        user_id: int,
        status: Optional[ModerationStatus] = None,
        content_type: Optional[ContentType] = None,
        skip: int = 0,
        limit: int = 50
    ) -> List[Report]:
        """
        Obtener lista de reportes con filtros
        """
        if not await ReportService._is_moderator(db, user_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only moderators can view reports"
            )

        query = db.query(Report)

        if status:
            query = query.filter(Report.status == status)
        if content_type:
            query = query.filter(Report.content_type == content_type)

        return query.order_by(desc(Report.created_at))\
            .offset(skip)\
            .limit(limit)\
            .all()

    @staticmethod
    async def update_report_status(
        db: Session,
        report_id: int,
        moderator_id: int,
        new_status: ModerationStatus,
        action: Optional[ModerationAction] = None,
        notes: Optional[str] = None
    ) -> Report:
        """
        Actualizar el estado de un reporte
        """
        try:
            if not await ReportService._is_moderator(db, moderator_id):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Only moderators can update reports"
                )

            report = db.query(Report).filter(Report.report_id == report_id).first()
            if not report:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Report not found"
                )

            # Actualizar el reporte
            report.status = new_status
            report.moderated_by = moderator_id
            report.moderated_at = datetime.utcnow()
            
            if action:
                report.action_taken = action
            if notes:
                report.notes = notes

            # Aplicar la acción de moderación
            if action:
                await ReportService._apply_moderation_action(
                    db,
                    report.content_type,
                    report.content_id,
                    action
                )

            db.commit()
            db.refresh(report)

            return report

        except HTTPException:
            db.rollback()
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating report: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error updating report: {str(e)}"
            )

    @staticmethod
    async def _verify_content_exists(
        db: Session,
        content_type: ContentType,
        content_id: int
    ) -> bool:
        """Verificar si el contenido reportado existe"""
        try:
            if content_type == ContentType.POST:
                return db.query(Post).filter(Post.post_id == content_id).first() is not None
            elif content_type == ContentType.COMMENT:
                return db.query(Comment).filter(Comment.comment_id == content_id).first() is not None
            elif content_type == ContentType.GROUP:
                return db.query(Group).filter(Group.group_id == content_id).first() is not None
            elif content_type == ContentType.GROUP_POST:
                return db.query(GroupPost).filter(GroupPost.group_post_id == content_id).first() is not None
            elif content_type == ContentType.USER:
                return db.query(User).filter(User.user_id == content_id).first() is not None
            return False
        except Exception as e:
            logger.error(f"Error verifying content: {str(e)}")
            return False

    @staticmethod
    async def _is_moderator(db: Session, user_id: int) -> bool:
        """Verificar si un usuario es moderador"""
        try:
            user = db.query(User).filter(User.user_id == user_id).first()
            return user and user.role_id in [1, 2]  # Asumiendo que roles 1 y 2 son admin y moderador
        except Exception as e:
            logger.error(f"Error checking moderator status: {str(e)}")
            return False

    @staticmethod
    async def _check_for_auto_moderation(db: Session, report: Report) -> None:
        """
        Verificar si se debe aplicar auto-moderación basada en número de reportes
        o severidad del contenido
        """
        try:
            # Contar reportes similares
            similar_reports = db.query(func.count(Report.report_id))\
                .filter(
                    Report.content_type == report.content_type,
                    Report.content_id == report.content_id,
                    Report.status == ModerationStatus.PENDING
                ).scalar()

            # Auto-moderar si hay muchos reportes
            if similar_reports >= 5:  # Umbral configurable
                report.status = ModerationStatus.AUTO_FLAGGED
                db.commit()

        except Exception as e:
            logger.error(f"Error in auto moderation: {str(e)}")

    @staticmethod
    async def _apply_moderation_action(
        db: Session,
        content_type: ContentType,
        content_id: int,
        action: ModerationAction
    ) -> None:
        """
        Aplicar la acción de moderación al contenido
        """
        try:
            if action == ModerationAction.REMOVE_CONTENT:
                if content_type == ContentType.POST:
                    post = db.query(Post).filter(Post.post_id == content_id).first()
                    if post:
                        db.delete(post)
                elif content_type == ContentType.COMMENT:
                    comment = db.query(Comment).filter(Comment.comment_id == content_id).first()
                    if comment:
                        db.delete(comment)
                # Implementar otros tipos de contenido...

            elif action == ContentType.TEMPORARY_BAN:
                if content_type == ContentType.USER:
                    user = db.query(User).filter(User.user_id == content_id).first()
                    if user:
                        user.status = False
                        user.banned_until = datetime.utcnow() + timedelta(days=7)  # Configurable

            elif action == ModerationAction.PERMANENT_BAN:
                if content_type == ContentType.USER:
                    user = db.query(User).filter(User.user_id == content_id).first()
                    if user:
                        user.status = False
                        user.banned_until = None  # Ban permanente

            db.commit()

        except Exception as e:
            db.rollback()
            logger.error(f"Error applying moderation action: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error applying moderation action: {str(e)}"
            )