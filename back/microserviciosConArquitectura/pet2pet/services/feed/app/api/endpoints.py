from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta

from shared.database.session import get_db
from shared.database.models import User
from services.auth.app.api.dependencies import get_current_active_user
from services.feed.app.models.schemas import (
    FeedType, ContentType, FeedResponse, FeedFilters,
    FeedPreferences, FeedAction, FeedItem
)
from services.feed.app.services.feed_service import FeedService
from services.feed.app.services.aggregator_service import AggregatorService
from services.feed.app.services.ranking_service import RankingService

router = APIRouter()

@router.get("/", response_model=FeedResponse)
async def get_feed(
    feed_type: FeedType = Query(FeedType.MAIN, description="Tipo de feed a obtener"),
    page: int = Query(1, ge=1, description="Número de página"),
    page_size: int = Query(20, ge=1, le=50, description="Resultados por página"),
    content_types: Optional[List[ContentType]] = Query(None, description="Tipos de contenido a incluir"),
    pet_id: Optional[int] = Query(None, description="Filtrar por mascota específica"),
    group_id: Optional[int] = Query(None, description="Filtrar por grupo específico"),
    location: Optional[str] = Query(None, description="Filtrar por ubicación"),
    date_from: Optional[datetime] = Query(None, description="Fecha inicial"),
    date_to: Optional[datetime] = Query(None, description="Fecha final"),
    tags: Optional[List[str]] = Query(None, description="Filtrar por tags"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Obtener feed personalizado con filtros opcionales.
    El feed puede ser principal, de seguidos, de grupos o trending.
    """
    filters = FeedFilters(
        feed_type=feed_type,
        content_types=content_types,
        pet_id=pet_id,
        group_id=group_id,
        location=location,
        date_from=date_from,
        date_to=date_to,
        tags=tags
    )
    return await FeedService.get_feed(
        db,
        current_user.user_id,
        filters,
        page,
        page_size
    )

@router.get("/trending", response_model=FeedResponse)
async def get_trending_feed(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=50),
    time_window: str = Query("24h", description="Ventana de tiempo (24h, 7d, 30d)"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Obtener feed de contenido trending.
    Ordena el contenido por popularidad en una ventana de tiempo.
    """
    filters = FeedFilters(
        feed_type=FeedType.TRENDING,
        content_types=[ContentType.POST, ContentType.GROUP_POST]
    )
    
    # Convertir ventana de tiempo a datetime
    time_windows = {
        "24h": timedelta(hours=24),
        "7d": timedelta(days=7),
        "30d": timedelta(days=30)
    }
    if time_window in time_windows:
        filters.date_from = datetime.utcnow() - time_windows[time_window]
    
    return await FeedService.get_feed(
        db,
        current_user.user_id,
        filters,
        page,
        page_size
    )

@router.get("/following", response_model=FeedResponse)
async def get_following_feed(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=50),
    pet_id: Optional[int] = Query(None, description="Ver feed de una mascota específica"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Obtener feed de mascotas seguidas.
    Opcionalmente filtrar por una mascota específica del usuario.
    """
    filters = FeedFilters(
        feed_type=FeedType.FOLLOWING,
        pet_id=pet_id
    )
    return await FeedService.get_feed(
        db,
        current_user.user_id,
        filters,
        page,
        page_size
    )

@router.get("/groups", response_model=FeedResponse)
async def get_groups_feed(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=50),
    group_id: Optional[int] = Query(None, description="Ver feed de un grupo específico"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Obtener feed de grupos.
    Opcionalmente filtrar por un grupo específico.
    """
    filters = FeedFilters(
        feed_type=FeedType.GROUPS,
        group_id=group_id
    )
    return await FeedService.get_feed(
        db,
        current_user.user_id,
        filters,
        page,
        page_size
    )

@router.post("/preferences", status_code=status.HTTP_200_OK)
async def update_feed_preferences(
    preferences: FeedPreferences,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Actualizar preferencias de feed del usuario.
    Esto afectará la forma en que se ordena y filtra el contenido.
    """
    return await FeedService.update_preferences(
        db,
        current_user.user_id,
        preferences
    )

@router.get("/preferences", response_model=FeedPreferences)
async def get_feed_preferences(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Obtener preferencias actuales del feed del usuario.
    """
    return await FeedService.get_preferences(
        db,
        current_user.user_id
    )

@router.post("/action", status_code=status.HTTP_200_OK)
async def record_feed_action(
    action: FeedAction,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Registrar una acción del usuario en el feed (like, share, hide, etc.).
    Esto ayuda a mejorar la personalización del feed.
    """
    return await FeedService.record_action(
        db,
        current_user.user_id,
        action
    )

@router.get("/refresh/{item_id}", response_model=FeedItem)
async def refresh_feed_item(
    item_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Actualizar un item específico del feed.
    Útil para actualizar contadores o contenido en tiempo real.
    """
    return await FeedService.refresh_item(
        db,
        item_id,
        current_user.user_id
    )

@router.post("/hide/{item_id}", status_code=status.HTTP_200_OK)
async def hide_feed_item(
    item_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Ocultar un item del feed.
    El item no aparecerá en futuros feeds del usuario.
    """
    return await FeedService.hide_item(
        db,
        item_id,
        current_user.user_id
    )