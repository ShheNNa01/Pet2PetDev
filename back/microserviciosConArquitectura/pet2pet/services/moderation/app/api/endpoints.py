# services/moderation/app/api/endpoints.py
from datetime import timedelta
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional

from services.moderation.app.models.schemas import (
    AutoModResult,
    ContentFilter,
    ContentStatus,
    FilterResult,
    ContentType,
    ModerationAction,
    ModerationStats,
    ModerationStatus,
    ContentReview,
    FilterConfiguration,
    CustomFilterRule,
    ReportCreate,
    ReportResponse,
    ReportUpdate
)
from services.moderation.app.services.content_filter_service import ContentFilterService
from services.moderation.app.api.dependencies import get_content_filter_service, get_current_moderator, get_moderation_service, get_queue_service, get_report_service
from services.moderation.app.services.moderation_service import ModerationService
from services.moderation.app.services.queue_service import QueueService
from services.moderation.app.services.report_service import ReportService
from shared.database.session import get_db
from shared.database.models import Report, User

router = APIRouter()

# Rutas de Reportes
@router.post("/reports", response_model=ReportResponse, status_code=status.HTTP_201_CREATED)
async def create_report(
    report: ReportCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_moderator),
    report_service: ReportService = Depends(get_report_service),
    queue_service: QueueService = Depends(get_queue_service)
):
    """
    Crea un nuevo reporte y lo añade a la cola de moderación.
    """
    # Crear el reporte
    new_report = await report_service.create_report(db, report, current_user.user_id)
    
    # Añadir a la cola de moderación en segundo plano
    background_tasks.add_task(
        queue_service.add_to_queue,
        db,
        new_report.reported_content_id,
        report.content_type,
        0.5,  # Prioridad inicial media
        current_user.trust_score if hasattr(current_user, 'trust_score') else 0.5
    )
    
    return new_report

@router.get("/reports", response_model=List[ReportResponse])
async def get_reports(
    status: Optional[ContentStatus] = None,
    content_type: Optional[ContentType] = None,
    priority: bool = False,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_moderator),
    report_service: ReportService = Depends(get_report_service)
):
    """
    Obtiene la lista de reportes con filtros opcionales.
    """
    if priority:
        return await report_service.get_pending_reports(db, content_type, priority=True)
    
    reports = db.query(Report)
    if status:
        reports = reports.filter(Report.status == status)
    if content_type:
        reports = reports.filter(Report.content_type == content_type)
    
    return reports.offset(skip).limit(limit).all()

@router.get("/reports/{report_id}", response_model=ReportResponse)
async def get_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_moderator),
    report_service: ReportService = Depends(get_report_service)
):
    """
    Obtiene los detalles de un reporte específico.
    """
    report = await report_service.get_report_details(db, report_id)
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )
    return report

@router.patch("/reports/{report_id}", response_model=ReportResponse)
async def update_report(
    report_id: int,
    report_update: ReportUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_moderator),
    report_service: ReportService = Depends(get_report_service)
):
    """
    Actualiza el estado de un reporte y ejecuta las acciones correspondientes.
    """
    report, success = await report_service.update_report_status(
        db,
        report_id,
        report_update.status,
        current_user.user_id,
        report_update.moderation_notes
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )
    return report

# Rutas de Cola de Moderación
@router.get("/queue/stats")
async def get_queue_stats(
    queue_service: QueueService = Depends(get_queue_service),
    current_user: User = Depends(get_current_moderator)
):
    """
    Obtiene estadísticas actuales de la cola de moderación.
    """
    return await queue_service.get_queue_stats()

@router.get("/queue/next", response_model=Optional[Dict])
async def get_next_queue_item(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_moderator),
    queue_service: QueueService = Depends(get_queue_service)
):
    """
    Obtiene el siguiente item de la cola para moderar.
    """
    return await queue_service.get_next_item(db)

# Rutas de Revisión de Contenido
@router.post("/content/review", response_model=AutoModResult)
async def review_content(
    content: ContentReview,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    moderation_service: ModerationService = Depends(get_moderation_service),
    queue_service: QueueService = Depends(get_queue_service)
):
    """
    Revisa automáticamente el contenido y lo añade a la cola si es necesario.
    """
    result = await moderation_service.review_content(db, content)
    
    # Si el contenido necesita revisión manual, añadirlo a la cola
    if not result.is_approved:
        background_tasks.add_task(
            queue_service.add_to_queue,
            db,
            content.content_id,
            content.content_type,
            1 - result.confidence_score,  # Alta prioridad para contenido sospechoso
            0.5
        )
    
    return result

# Rutas de Acciones de Moderación
@router.post("/actions", response_model=Dict)
async def take_moderation_action(
    action: ModerationAction,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_moderator),
    moderation_service: ModerationService = Depends(get_moderation_service)
):
    """
    Ejecuta una acción de moderación sobre contenido o usuario.
    """
    success, message = await moderation_service.take_moderation_action(db, action)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )
    return {"status": "success", "message": message}

# Rutas de Estadísticas y Reportes
@router.get("/stats", response_model=ModerationStats)
async def get_moderation_stats(
    time_range: int = 30,  # días
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_moderator),
    report_service: ReportService = Depends(get_report_service)
):
    """
    Obtiene estadísticas detalladas del sistema de moderación.
    """
    return await report_service.get_report_statistics(
        db,
        timedelta(days=time_range)
    )

@router.get("/users/{user_id}/history", response_model=Dict)
async def get_user_moderation_history(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_moderator),
    report_service: ReportService = Depends(get_report_service)
):
    """
    Obtiene el historial completo de moderación de un usuario.
    """
    reports_made = await report_service.get_user_report_history(db, user_id, as_reporter=True)
    reports_received = await report_service.get_user_report_history(db, user_id, as_reporter=False)
    
    return {
        "reports_made": reports_made,
        "reports_received": reports_received
    }

@router.post("/filter", response_model=FilterResult)
async def filter_content(
    content_review: ContentReview,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_moderator),
    content_filter: ContentFilterService = Depends(get_content_filter_service)
):
    """
    Filtra contenido basado en las reglas configuradas.
    
    - Verifica contenido inapropiado
    - Detecta spam y contenido malicioso
    - Aplica filtros personalizados
    """
    try:
        result = await content_filter.filter_content(
            content=content_review.content,
            content_type=content_review.content_type,
            settings=content_review.filter_settings
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/filter/batch", response_model=List[FilterResult])
async def filter_content_batch(
    content_reviews: List[ContentReview],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_moderator),
    content_filter: ContentFilterService = Depends(get_content_filter_service)
):
    """
    Filtra múltiples contenidos en una sola llamada.
    
    Útil para:
    - Verificación masiva de contenido
    - Procesamiento por lotes de comentarios o posts
    """
    results = []
    for review in content_reviews:
        try:
            result = await content_filter.filter_content(
                content=review.content,
                content_type=review.content_type,
                settings=review.filter_settings
            )
            results.append(result)
        except Exception as e:
            results.append(FilterResult(
                is_flagged=True,
                confidence_score=1.0,
                matched_filters=["error"],
                filtered_content=None,
                recommendations=[f"Error processing content: {str(e)}"]
            ))
    return results

@router.post("/filter/configurations", response_model=FilterConfiguration)
async def create_filter_configuration(
    config: FilterConfiguration,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_moderator)
):
    """
    Crea una nueva configuración de filtrado personalizada.
    
    Permite definir:
    - Niveles de sensibilidad
    - Palabras clave personalizadas
    - Reglas específicas por tipo de contenido
    """
    # Implementar lógica para guardar configuración en la base de datos
    pass

@router.get("/filter/configurations", response_model=List[FilterConfiguration])
async def get_filter_configurations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_moderator)
):
    """
    Obtiene todas las configuraciones de filtrado disponibles.
    """
    # Implementar lógica para obtener configuraciones
    pass

@router.get("/filter/configurations/{config_id}", response_model=FilterConfiguration)
async def get_filter_configuration(
    config_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_moderator)
):
    """
    Obtiene una configuración de filtrado específica.
    """
    # Implementar lógica para obtener configuración específica
    pass

@router.put("/filter/configurations/{config_id}", response_model=FilterConfiguration)
async def update_filter_configuration(
    config_id: int,
    config: FilterConfiguration,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_moderator)
):
    """
    Actualiza una configuración de filtrado existente.
    """
    # Implementar lógica para actualizar configuración
    pass

@router.post("/filter/custom-rules", response_model=CustomFilterRule)
async def create_custom_rule(
    rule: CustomFilterRule,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_moderator)
):
    """
    Crea una nueva regla de filtrado personalizada.
    
    Permite definir:
    - Palabras clave a detectar
    - Términos excluidos
    - Nivel de sensibilidad específico
    """
    # Implementar lógica para crear regla personalizada
    pass

@router.get("/filter/custom-rules", response_model=List[CustomFilterRule])
async def get_custom_rules(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_moderator)
):
    """
    Obtiene todas las reglas de filtrado personalizadas.
    """
    # Implementar lógica para obtener reglas personalizadas
    pass

@router.put("/filter/custom-rules/{rule_id}", response_model=CustomFilterRule)
async def update_custom_rule(
    rule_id: int,
    rule: CustomFilterRule,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_moderator)
):
    """
    Actualiza una regla de filtrado personalizada existente.
    """
    # Implementar lógica para actualizar regla personalizada
    pass

@router.delete("/filter/custom-rules/{rule_id}")
async def delete_custom_rule(
    rule_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_moderator)
):
    """
    Elimina una regla de filtrado personalizada.
    """
    # Implementar lógica para eliminar regla personalizada
    return {"status": "success", "message": "Rule deleted successfully"}