from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, func, desc, text
from datetime import datetime
import time
from typing import List, Dict, Any, Optional

from shared.database.models import (
    Pet, User, Post, Group, Comment, PetType, Breed,
    GroupMember, Follower, MediaFile
)
from ..models.schemas import (
    SearchQuery, SearchType, SearchResult,
    PetResult, UserResult, PostResult, GroupResult, CommentResult
)

class SearchService:
    @staticmethod
    async def search(
        db: Session,
        current_user_id: int,
        search_query: SearchQuery
    ) -> SearchResult:
        """Realizar búsqueda global o específica según los criterios"""
        start_time = time.time()
        try:
            results = SearchResult(
                pets=[],
                users=[],
                posts=[],
                groups=[],
                comments=[],
                total_results=0,
                page=search_query.page,
                total_pages=0,
                search_time=0,
                suggestions=[]
            )

            # Calcular offset para paginación
            offset = (search_query.page - 1) * search_query.page_size

            # Realizar búsqueda según el tipo
            if search_query.filters.type in [SearchType.ALL, SearchType.PETS]:
                pets_results = await SearchService._search_pets(
                    db, current_user_id, search_query, offset
                )
                results.pets = pets_results.get('items', [])
                if search_query.filters.type == SearchType.PETS:
                    results.total_results = pets_results.get('total', 0)
                    results.total_pages = -(-pets_results.get('total', 0) // search_query.page_size)

            if search_query.filters.type in [SearchType.ALL, SearchType.USERS]:
                users_results = await SearchService._search_users(
                    db, current_user_id, search_query, offset
                )
                results.users = users_results.get('items', [])
                if search_query.filters.type == SearchType.USERS:
                    results.total_results = users_results.get('total', 0)
                    results.total_pages = -(-users_results.get('total', 0) // search_query.page_size)

            if search_query.filters.type in [SearchType.ALL, SearchType.POSTS]:
                posts_results = await SearchService._search_posts(
                    db, current_user_id, search_query, offset
                )
                results.posts = posts_results.get('items', [])
                if search_query.filters.type == SearchType.POSTS:
                    results.total_results = posts_results.get('total', 0)
                    results.total_pages = -(-posts_results.get('total', 0) // search_query.page_size)

            if search_query.filters.type in [SearchType.ALL, SearchType.GROUPS]:
                groups_results = await SearchService._search_groups(
                    db, current_user_id, search_query, offset
                )
                results.groups = groups_results.get('items', [])
                if search_query.filters.type == SearchType.GROUPS:
                    results.total_results = groups_results.get('total', 0)
                    results.total_pages = -(-groups_results.get('total', 0) // search_query.page_size)

            # Si es búsqueda global, sumar todos los resultados
            if search_query.filters.type == SearchType.ALL:
                results.total_results = sum([
                    len(results.pets),
                    len(results.users),
                    len(results.posts),
                    len(results.groups),
                    len(results.comments)
                ])
                # Calcular páginas basado en el total de resultados
                results.total_pages = -(-results.total_results // search_query.page_size)

            # Calcular tiempo de búsqueda
            results.search_time = time.time() - start_time

            # Generar sugerencias si hay pocos resultados
            if results.total_results < 5:
                results.suggestions = await SearchService._generate_suggestions(
                    db, search_query.query
                )

            return results

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error performing search: {str(e)}"
            )

    @staticmethod
    async def _search_pets(
        db: Session,
        current_user_id: int,
        search_query: SearchQuery,
        offset: int
    ) -> Dict[str, Any]:
        query = db.query(Pet).join(User).outerjoin(Breed).outerjoin(PetType)

        # Aplicar filtros de búsqueda
        conditions = []
        conditions.append(Pet.status == True)  # Solo mascotas activas
        
        if search_query.query:
            conditions.append(or_(
                Pet.name.ilike(f"%{search_query.query}%"),
                Pet.bio.ilike(f"%{search_query.query}%"),
                Breed.breed_name.ilike(f"%{search_query.query}%"),
                PetType.type_name.ilike(f"%{search_query.query}%")
            ))

        if search_query.filters.breed_id:
            conditions.append(Pet.breed_id == search_query.filters.breed_id)

        if search_query.filters.pet_type_id:
            conditions.append(Breed.pet_type_id == search_query.filters.pet_type_id)

        query = query.filter(and_(*conditions))

        # Contar total antes de paginar
        total = query.count()

        # Aplicar ordenamiento
        if search_query.sort_by:
            sort_field = getattr(Pet, search_query.sort_by, Pet.created_at)
            query = query.order_by(
                desc(sort_field) if search_query.sort_order == "desc" else sort_field
            )
        else:
            query = query.order_by(Pet.created_at.desc())

        # Aplicar paginación
        query = query.offset(offset).limit(search_query.page_size)

        pets = query.all()

        # Convertir a PetResult
        results = []
        for pet in pets:
            results.append(PetResult(
                pet_id=pet.pet_id,
                name=pet.name,
                pet_picture=pet.pet_picture,
                breed_name=pet.breed.breed_name if pet.breed else None,
                pet_type=pet.breed.pet_type.type_name if pet.breed and pet.breed.pet_type else None,
                user_id=pet.user_id,
                owner_name=f"{pet.user.user_name} {pet.user.user_last_name}",
                score=1.0  # Implementar scoring más sofisticado en el futuro
            ))

        return {
            "items": results,
            "total": total
        }

    @staticmethod
    async def _generate_suggestions(db: Session, query: str) -> List[str]:
        """Generar sugerencias de búsqueda basadas en el término de búsqueda"""
        suggestions = []
        
        # Implementar lógica de sugerencias aquí
        # Por ejemplo, buscar términos similares en nombres de mascotas
        similar_names = db.query(Pet.name)\
            .filter(Pet.name.ilike(f"{query}%"))\
            .distinct()\
            .limit(5)\
            .all()
        
        suggestions.extend([name[0] for name in similar_names])

        return suggestions[:5]  # Limitar a 5 sugerencias

    @staticmethod
    async def _search_users(
        db: Session,
        current_user_id: int,
        search_query: SearchQuery,
        offset: int
    ) -> Dict[str, Any]:
        """Búsqueda de usuarios"""
        query = db.query(User)

        conditions = []
        conditions.append(User.status == True)  # Solo usuarios activos

        if search_query.query:
            conditions.append(or_(
                User.user_name.ilike(f"%{search_query.query}%"),
                User.user_last_name.ilike(f"%{search_query.query}%"),
                User.user_email.ilike(f"%{search_query.query}%"),
                User.user_bio.ilike(f"%{search_query.query}%")
            ))

        query = query.filter(and_(*conditions))
        total = query.count()

        # Ordenar
        if search_query.sort_by:
            sort_field = getattr(User, search_query.sort_by, User.created_at)
            query = query.order_by(
                desc(sort_field) if search_query.sort_order == "desc" else sort_field
            )
        else:
            query = query.order_by(User.created_at.desc())

        query = query.offset(offset).limit(search_query.page_size)
        users = query.all()

        results = []
        for user in users:
            pet_count = db.query(Pet).filter(Pet.user_id == user.user_id).count()
            results.append(UserResult(
                user_id=user.user_id,
                user_name=user.user_name,
                user_last_name=user.user_last_name,
                profile_picture=user.profile_picture,
                pet_count=pet_count,
                score=1.0
            ))

        return {
            "items": results,
            "total": total
        }

    @staticmethod
    async def _search_posts(
        db: Session,
        current_user_id: int,
        search_query: SearchQuery,
        offset: int
    ) -> Dict[str, Any]:
        """Búsqueda de posts"""
        query = db.query(Post).join(User).outerjoin(Pet).outerjoin(MediaFile)

        conditions = []
        if search_query.query:
            conditions.append(or_(
                Post.content.ilike(f"%{search_query.query}%"),
                Post.location.ilike(f"%{search_query.query}%")
            ))

        if search_query.filters.date_from:
            conditions.append(Post.created_at >= search_query.filters.date_from)
        if search_query.filters.date_to:
            conditions.append(Post.created_at <= search_query.filters.date_to)

        query = query.filter(and_(*conditions))
        total = query.count()

        # Ordenar
        query = query.order_by(Post.created_at.desc())
        query = query.offset(offset).limit(search_query.page_size)
        posts = query.all()

        results = []
        for post in posts:
            media_urls = [media.media_url for media in post.media_files]
            results.append(PostResult(
                post_id=post.post_id,
                content=post.content,
                user_id=post.user_id,
                pet_id=post.pet_id,
                created_at=post.created_at,
                media_urls=media_urls,
                author_name=f"{post.user.user_name} {post.user.user_last_name}",
                pet_name=post.pet.name if post.pet else None,
                score=1.0
            ))

        return {
            "items": results,
            "total": total
        }

    @staticmethod
    async def _search_groups(
        db: Session,
        current_user_id: int,
        search_query: SearchQuery,
        offset: int
    ) -> Dict[str, Any]:
        """Búsqueda de grupos"""
        query = db.query(Group)

        conditions = []
        if search_query.query:
            conditions.append(or_(
                Group.name_group.ilike(f"%{search_query.query}%"),
                Group.description.ilike(f"%{search_query.query}%")
            ))

        # Solo mostrar grupos públicos o grupos privados donde el usuario es miembro
        private_groups = Group.group_id.in_(
            db.query(GroupMember.group_id).filter(GroupMember.user_id == current_user_id)
        )
        conditions.append(or_(
            Group.privacy == False,
            private_groups
        ))

        query = query.filter(and_(*conditions))
        total = query.count()

        query = query.order_by(Group.created_at.desc())
        query = query.offset(offset).limit(search_query.page_size)
        groups = query.all()

        results = []
        for group in groups:
            member_count = db.query(GroupMember).filter(
                GroupMember.group_id == group.group_id
            ).count()
            
            results.append(GroupResult(
                group_id=group.group_id,
                name_group=group.name_group,
                description=group.description,
                group_picture=group.group_picture,
                member_count=member_count,
                privacy=group.privacy,
                score=1.0
            ))

        return {
            "items": results,
            "total": total
        }

    @staticmethod
    async def get_suggestions(
        db: Session,
        query: str,
        search_type: SearchType = SearchType.ALL
    ) -> List[str]:
        """Obtener sugerencias de búsqueda"""
        suggestions = set()
        
        if search_type in [SearchType.ALL, SearchType.PETS]:
            pet_suggestions = db.query(Pet.name)\
                .filter(Pet.name.ilike(f"{query}%"))\
                .distinct()\
                .limit(3)\
                .all()
            suggestions.update([name[0] for name in pet_suggestions])

        if search_type in [SearchType.ALL, SearchType.USERS]:
            user_suggestions = db.query(User.user_name)\
                .filter(User.user_name.ilike(f"{query}%"))\
                .distinct()\
                .limit(3)\
                .all()
            suggestions.update([name[0] for name in user_suggestions])

        if search_type in [SearchType.ALL, SearchType.GROUPS]:
            group_suggestions = db.query(Group.name_group)\
                .filter(Group.name_group.ilike(f"{query}%"))\
                .distinct()\
                .limit(3)\
                .all()
            suggestions.update([name[0] for name in group_suggestions])

        return list(suggestions)[:5]

    @staticmethod
    async def get_trending_searches(
        db: Session,
        search_type: Optional[SearchType] = None
    ) -> List[str]:
        """
        Obtener búsquedas tendencia
        Aquí podrías implementar la lógica para obtener las búsquedas más populares
        Por ahora retornamos una lista estática
        """
        # En una implementación real, esto vendría de una tabla de búsquedas
        trending = [
            "perros",
            "gatos",
            "veterinarias",
            "adopción",
            "cuidados mascota"
        ]
        return trending

    @staticmethod
    async def get_recent_searches(
        db: Session,
        user_id: int
    ) -> List[str]:
        """
        Obtener búsquedas recientes del usuario
        En una implementación completa, necesitarías una tabla para almacenar el historial
        """
        return []  # Implementar cuando se agregue la tabla de historial