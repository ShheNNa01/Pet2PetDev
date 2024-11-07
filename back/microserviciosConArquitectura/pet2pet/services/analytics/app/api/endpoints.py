# services/analytics/app/api/endpoints.py
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, Query, status, BackgroundTasks
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import logging

from services.analytics.app.core.decorators import cached
from services.analytics.app.core.cache import cache
from services.analytics.app.core.config import settings
from services.analytics.app.models.schemas import (
    MetricValue,
    TimeRange,
    DateRange,
    AnalyticsFilter,
    TimeSeriesMetric,
    UserActivityMetrics,
    ContentMetrics,
    EngagementMetrics,
    PlatformMetrics,
    DashboardMetrics
)
from services.analytics.app.api.dependencies import (
    get_user_analytics_service,
    get_content_analytics_service,
    get_engagement_analytics_service,
    get_platform_analytics_service
)
from services.analytics.app.services.export_service import ExportService
from shared.database.session import get_db

logger = logging.getLogger(__name__)
router = APIRouter()

async def verify_cache_status():
    """Verifica el estado del caché y registra cualquier problema"""
    if not cache.check_health() and settings.CACHE_ENABLED:
        logger.warning("Cache is enabled in settings but Redis is not available")

# Dashboard General
@router.get("/dashboard", response_model=DashboardMetrics)
@cached("dashboard", ttl=timedelta(minutes=5))
async def get_dashboard_metrics(
    time_range: TimeRange = Query(TimeRange.DAY),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
    user_analytics = Depends(get_user_analytics_service),
    content_analytics = Depends(get_content_analytics_service),
    engagement_analytics = Depends(get_engagement_analytics_service),
    platform_analytics = Depends(get_platform_analytics_service)
):
    """
    Obtiene todas las métricas principales para el dashboard.
    Cache: 5 minutos
    """
    try:
        await verify_cache_status()
        
        if start_date and end_date and start_date > end_date:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="start_date must be before end_date"
            )

        # Obtener todas las métricas
        user_metrics = await user_analytics.get_user_activity_metrics(
            db, time_range, start_date, end_date
        )
        content_metrics = await content_analytics.get_content_metrics(
            db, time_range, start_date, end_date
        )
        engagement_metrics = await engagement_analytics.get_engagement_metrics(
            db, time_range, start_date, end_date
        )
        platform_metrics = await platform_analytics.get_platform_metrics(
            db, time_range, start_date, end_date
        )

        # Construir y retornar el dashboard
        dashboard = DashboardMetrics(
            user_metrics=user_metrics,
            content_metrics=content_metrics,
            engagement_metrics=engagement_metrics,
            platform_metrics=platform_metrics
        )

        return dashboard

    except Exception as e:
        logger.error(f"Error getting dashboard metrics: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

# Métricas de Usuarios
@router.get("/users", response_model=UserActivityMetrics)
@cached("user_metrics", ttl=timedelta(minutes=10))
async def get_user_metrics(
    time_range: TimeRange = Query(TimeRange.DAY),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
    user_analytics = Depends(get_user_analytics_service)
):
    """
    Obtiene métricas detalladas de actividad de usuarios.
    Cache: 10 minutos si Redis está disponible
    """
    try:
        await verify_cache_status()
        return await user_analytics.get_user_activity_metrics(
            db, time_range, start_date, end_date
        )
    except Exception as e:
        logger.error(f"Error getting user metrics: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/users/growth", response_model=Dict)
async def get_user_growth(
    time_range: TimeRange = Query(TimeRange.MONTH),
    granularity: str = Query("day"),
    db: Session = Depends(get_db),
    user_analytics = Depends(get_user_analytics_service)
):
    """
    Obtiene datos de crecimiento de usuarios en el tiempo.
    Sin caché para datos en tiempo real
    """
    try:
        metrics = await user_analytics.get_user_activity_metrics(
            db, time_range, None, None
        )
        return {
            "growth_data": metrics.user_growth.data,
            "total_growth": metrics.user_growth.total,
            "average_growth": metrics.user_growth.average
        }
    except Exception as e:
        logger.error(f"Error getting user growth: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

# Métricas de Contenido
@router.get("/content", response_model=ContentMetrics)
@cached("content_metrics", ttl=timedelta(minutes=15))
async def get_content_metrics(
    time_range: TimeRange = Query(TimeRange.DAY),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
    content_analytics = Depends(get_content_analytics_service)
):
    """
    Obtiene métricas detalladas sobre el contenido.
    Cache: 15 minutos si Redis está disponible
    """
    try:
        await verify_cache_status()
        return await content_analytics.get_content_metrics(
            db, time_range, start_date, end_date
        )
    except Exception as e:
        logger.error(f"Error getting content metrics: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/content/popular-categories", response_model=List[Dict[str, float]])
async def get_popular_categories(
    time_range: TimeRange = Query(TimeRange.WEEK),
    db: Session = Depends(get_db),
    content_analytics = Depends(get_content_analytics_service)
):
    """
    Obtiene las categorías más populares de contenido.
    Sin caché para datos actualizados
    """
    try:
        metrics = await content_analytics.get_content_metrics(
            db, time_range, None, None
        )
        return metrics.popular_categories
    except Exception as e:
        logger.error(f"Error getting popular categories: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

# Métricas de Engagement
@router.get("/engagement", response_model=EngagementMetrics)
@cached("engagement_metrics", ttl=timedelta(minutes=10))
async def get_engagement_metrics(
    time_range: TimeRange = Query(TimeRange.DAY),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
    engagement_analytics = Depends(get_engagement_analytics_service)
):
    """
    Obtiene métricas detalladas de engagement.
    Cache: 10 minutos si Redis está disponible
    """
    try:
        await verify_cache_status()
        return await engagement_analytics.get_engagement_metrics(
            db, time_range, start_date, end_date
        )
    except Exception as e:
        logger.error(f"Error getting engagement metrics: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/engagement/peak-hours", response_model=List[Dict[str, float]])
async def get_peak_hours(
    time_range: TimeRange = Query(TimeRange.WEEK),
    db: Session = Depends(get_db),
    engagement_analytics = Depends(get_engagement_analytics_service)
):
    """Obtiene las horas de mayor actividad."""
    try:
        metrics = await engagement_analytics.get_engagement_metrics(
            db, time_range, None, None
        )
        return metrics.peak_activity_hours
    except Exception as e:
        logger.error(f"Error getting peak hours: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/engagement/user-segments", response_model=List[Dict[str, float]])
async def get_user_segments(
    time_range: TimeRange = Query(TimeRange.MONTH),
    db: Session = Depends(get_db),
    engagement_analytics = Depends(get_engagement_analytics_service)
):
    """Obtiene segmentación de usuarios por nivel de engagement."""
    try:
        metrics = await engagement_analytics.get_engagement_metrics(
            db, time_range, None, None
        )
        return metrics.user_segments
    except Exception as e:
        logger.error(f"Error getting user segments: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

# Métricas de Plataforma
@router.get("/platform", response_model=PlatformMetrics)
@cached("platform_metrics", ttl=timedelta(minutes=1))
async def get_platform_metrics(
    time_range: TimeRange = Query(TimeRange.DAY),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
    platform_analytics = Depends(get_platform_analytics_service)
):
    """
    Obtiene métricas detalladas del rendimiento de la plataforma.
    Cache: 1 minuto si Redis está disponible
    """
    try:
        await verify_cache_status()
        return await platform_analytics.get_platform_metrics(
            db, time_range, start_date, end_date
        )
    except Exception as e:
        logger.error(f"Error getting platform metrics: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/platform/health", response_model=Dict[str, MetricValue])
async def get_system_health(
    platform_analytics = Depends(get_platform_analytics_service)
):
    """
    Obtiene el estado actual de salud del sistema.
    Sin caché para datos en tiempo real
    """
    try:
        return await platform_analytics.get_system_health_metrics()
    except Exception as e:
        logger.error(f"Error getting system health: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

# Configuración del servicio de exportación
export_service = ExportService()

# Endpoints de exportación
@router.post("/export")
async def export_metrics(
    background_tasks: BackgroundTasks,
    metrics_type: str = Query(..., description="Type of metrics to export: users, content, engagement, platform"),
    time_range: TimeRange = Query(TimeRange.MONTH),
    format: str = Query("csv", regex="^(csv|xlsx|json)$"),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """Inicia la exportación de métricas en segundo plano."""
    try:
        job_id = f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{metrics_type}"
        
        background_tasks.add_task(
            export_service.export_data,
            db,
            metrics_type,
            time_range,
            format,
            start_date,
            end_date
        )
        
        return {
            "message": "Export started",
            "job_id": job_id,
            "status_url": f"/api/v1/analytics/export/status/{job_id}"
        }
    except Exception as e:
        logger.error(f"Error starting export: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/export/status/{job_id}")
async def get_export_status(job_id: str):
    """Verifica el estado de un trabajo de exportación."""
    try:
        return await export_service.get_export_status(job_id)
    except Exception as e:
        logger.error(f"Error getting export status: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/exports/{filename}")
async def get_export_file(filename: str):
    """Descarga un archivo de exportación."""
    file_path = Path("exports") / filename
    if not file_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Export file not found"
        )
    
    return FileResponse(
        file_path,
        filename=filename,
        media_type='application/octet-stream'
    )

@router.post("/export/cleanup")
async def cleanup_exports(
    background_tasks: BackgroundTasks,
    max_age_hours: int = Query(24, ge=1, le=168)
):
    """Limpia archivos de exportación antiguos."""
    try:
        background_tasks.add_task(export_service.clean_old_exports, max_age_hours)
        return {"message": "Cleanup started"}
    except Exception as e:
        logger.error(f"Error starting cleanup: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )