# services/analytics/app/services/export_service.py
import csv
import json
import pandas as pd
from io import StringIO
from typing import Dict, Any, List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
import asyncio
import aiofiles
import logging
from pathlib import Path

from services.analytics.app.models.schemas import TimeRange
from services.analytics.app.services.content_analytics import ContentAnalyticsService
from services.analytics.app.services.engagement_analytics import (
    EngagementAnalyticsService,
)
from services.analytics.app.services.platform_analytics import PlatformAnalyticsService
from services.analytics.app.services.user_analytics import UserAnalyticsService


logger = logging.getLogger(__name__)


class ExportService:
    def __init__(self):
        self.user_analytics = UserAnalyticsService()
        self.content_analytics = ContentAnalyticsService()
        self.engagement_analytics = EngagementAnalyticsService()
        self.platform_analytics = PlatformAnalyticsService()
        self.export_path = Path("exports")
        self.export_path.mkdir(exist_ok=True)

    async def export_data(
        self,
        db: Session,
        metrics_type: str,
        time_range: TimeRange,
        format: str = "csv",
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> str:
        """
        Exporta datos de métricas al formato especificado
        Returns: URL del archivo generado
        """
        try:
            # Obtener datos según el tipo
            data = await self._get_metrics_data(
                db, metrics_type, time_range, start_date, end_date
            )

            # Generar nombre de archivo único
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{metrics_type}_{timestamp}.{format}"
            filepath = self.export_path / filename

            # Exportar según formato
            if format == "csv":
                await self._export_to_csv(data, filepath)
            elif format == "xlsx":
                await self._export_to_excel(data, filepath)
            elif format == "json":
                await self._export_to_json(data, filepath)
            else:
                raise ValueError(f"Unsupported format: {format}")

            # Devolver URL relativa del archivo
            return f"/exports/{filename}"

        except Exception as e:
            logger.error(f"Error exporting {metrics_type} data: {str(e)}")
            raise

    async def _get_metrics_data(
        self,
        db: Session,
        metrics_type: str,
        time_range: TimeRange,
        start_date: Optional[datetime],
        end_date: Optional[datetime],
    ) -> Dict[str, Any]:
        """Obtiene los datos según el tipo de métrica"""
        if metrics_type == "users":
            metrics = await self.user_analytics.get_user_activity_metrics(
                db, time_range, start_date, end_date
            )
            return self._format_user_metrics(metrics)

        elif metrics_type == "content":
            metrics = await self.content_analytics.get_content_metrics(
                db, time_range, start_date, end_date
            )
            return self._format_content_metrics(metrics)

        elif metrics_type == "engagement":
            metrics = await self.engagement_analytics.get_engagement_metrics(
                db, time_range, start_date, end_date
            )
            return self._format_engagement_metrics(metrics)

        elif metrics_type == "platform":
            metrics = await self.platform_analytics.get_platform_metrics(
                db, time_range, start_date, end_date
            )
            return self._format_platform_metrics(metrics)

        else:
            raise ValueError(f"Unknown metrics type: {metrics_type}")

    def _format_user_metrics(self, metrics: Any) -> Dict[str, Any]:
        """Formatea métricas de usuarios para exportación"""
        return {
            "General Statistics": {
                "Total Users": metrics.total_users.value,
                "Active Users": metrics.active_users.value,
                "New Registrations": metrics.new_registrations.value,
                "Retention Rate": f"{metrics.retention_rate.value}%",
                "Churn Rate": f"{metrics.churn_rate.value}%",
            },
            "Growth Timeline": [
                {
                    "Date": point.timestamp.strftime("%Y-%m-%d %H:%M"),
                    "New Users": point.value,
                }
                for point in metrics.user_growth.data
            ],
        }

    def _format_content_metrics(self, metrics: Any) -> Dict[str, Any]:
        """Formatea métricas de contenido para exportación"""
        return {
            "Content Overview": {
                "Total Posts": metrics.total_posts.value,
                "Engagement Rate": f"{metrics.engagement_rate.value}%",
            },
            "Content Distribution": metrics.content_distribution,
            "Popular Categories": metrics.popular_categories,
            "Posting Timeline": [
                {
                    "Date": point.timestamp.strftime("%Y-%m-%d %H:%M"),
                    "Posts": point.value,
                }
                for point in metrics.posting_frequency.data
            ],
        }

    def _format_engagement_metrics(self, metrics: Any) -> Dict[str, Any]:
        """Formatea métricas de engagement para exportación"""
        return {
            "Engagement Overview": {
                "Total Interactions": metrics.total_interactions.value,
                "Average Session Duration": metrics.avg_session_duration.value,
            },
            "Interaction Types": metrics.interaction_types,
            "User Segments": metrics.user_segments,
            "Engagement Timeline": [
                {
                    "Date": point.timestamp.strftime("%Y-%m-%d %H:%M"),
                    "Interactions": point.value,
                }
                for point in metrics.engagement_by_time.data
            ],
        }

    def _format_platform_metrics(self, metrics: Any) -> Dict[str, Any]:
        """Formatea métricas de plataforma para exportación"""
        return {
            "System Health": {
                metric: value.value for metric, value in metrics.system_health.items()
            },
            "Resource Usage": {
                metric: value.value for metric, value in metrics.resource_usage.items()
            },
            "Error Rates": [
                {
                    "Date": point.timestamp.strftime("%Y-%m-%d %H:%M"),
                    "Error Rate": point.value,
                }
                for point in metrics.error_rates.data
            ],
        }

    async def _export_to_csv(self, data: Dict[str, Any], filepath: Path):
        """Exporta datos a CSV"""
        df = pd.json_normalize(data, sep="_")
        await asyncio.to_thread(df.to_csv, filepath, index=False)

    async def _export_to_excel(self, data: Dict[str, Any], filepath: Path):
        """Exporta datos a Excel"""
        df = pd.json_normalize(data, sep="_")
        await asyncio.to_thread(df.to_excel, filepath, index=False)

    async def _export_to_json(self, data: Dict[str, Any], filepath: Path):
        """Exporta datos a JSON"""
        async with aiofiles.open(filepath, "w") as f:
            await f.write(json.dumps(data, indent=2))

    async def get_export_status(self, job_id: str) -> Dict[str, Any]:
        """Obtiene el estado de un trabajo de exportación"""
        # En una implementación real, esto consultaría una cola de trabajos
        # Por ahora, simulamos que el trabajo está completo
        return {
            "status": "completed",
            "progress": 100,
            "download_url": f"/exports/{job_id}",
        }

    async def clean_old_exports(self, max_age_hours: int = 24):
        """Limpia exportaciones antiguas"""
        try:
            current_time = datetime.now()
            for file_path in self.export_path.glob("*.*"):
                file_age = datetime.fromtimestamp(file_path.stat().st_mtime)
                if (current_time - file_age).total_seconds() > max_age_hours * 3600:
                    file_path.unlink()
        except Exception as e:
            logger.error(f"Error cleaning old exports: {str(e)}")
