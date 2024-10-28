from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from services.search.app.services.indexer_service import IndexerService
from shared.database.session import get_db
from shared.database.models import User
from services.auth.app.api.dependencies import get_current_active_user
from services.search.app.models.schemas import (
    SearchQuery, SearchResult, SearchType,
    SortOrder, SearchFilters
)
from services.search.app.services.search_service import SearchService

router = APIRouter()

@router.post("/", response_model=SearchResult)
async def search(
    search_query: SearchQuery,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Búsqueda global o específica según los criterios proporcionados.
    """
    return await SearchService.search(db, current_user.user_id, search_query)

@router.get("/quick", response_model=SearchResult)
async def quick_search(
    q: str = Query(..., min_length=1, description="Término de búsqueda"),
    type: SearchType = Query(default=SearchType.ALL, description="Tipo de búsqueda"),
    page: int = Query(default=1, ge=1, description="Número de página"),
    page_size: int = Query(default=10, ge=1, le=50, description="Resultados por página"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Búsqueda rápida con parámetros simplificados.
    """
    search_query = SearchQuery(
        query=q,
        filters=SearchFilters(type=type),
        page=page,
        page_size=page_size
    )
    return await SearchService.search(db, current_user.user_id, search_query)

@router.get("/suggestions", response_model=List[str])
async def get_suggestions(
    q: str = Query(..., min_length=1, description="Término para sugerencias"),
    type: SearchType = Query(default=SearchType.ALL, description="Tipo de contenido"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Obtener sugerencias de búsqueda basadas en un término.
    """
    return await SearchService.get_suggestions(db, q, type)

@router.get("/trending", response_model=List[str])
async def get_trending_searches(
    type: Optional[SearchType] = Query(None, description="Tipo de contenido específico"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Obtener las búsquedas más populares.
    """
    return await SearchService.get_trending_searches(db, type)

@router.get("/recent", response_model=List[str])
async def get_recent_searches(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Obtener las búsquedas recientes del usuario.
    """
    return await SearchService.get_recent_searches(db, current_user.user_id)


@router.post("/index/{content_type}/{content_id}", status_code=status.HTTP_200_OK)
async def index_content(
        content_type: str,
        content_id: int,
        current_user: User = Depends(get_current_active_user),
        db: Session = Depends(get_db)
    ):
        """
        Indexar contenido específico.
        Solo para administradores.
        """
        if not current_user.role_id == 1:  # Asumiendo que role_id 1 es admin
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only administrators can manage index"
            )
        
        success = await IndexerService.index_new_content(db, content_type, content_id)
        return {"status": "success" if success else "error"}

@router.post("/reindex", status_code=status.HTTP_200_OK)
async def reindex_all(
        current_user: User = Depends(get_current_active_user),
        db: Session = Depends(get_db)
    ):
        """
        Reindexar todo el contenido.
        Solo para administradores.
        """
        if not current_user.role_id == 1:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only administrators can manage index"
            )
        
        results = await IndexerService.reindex_all(db)
        return results