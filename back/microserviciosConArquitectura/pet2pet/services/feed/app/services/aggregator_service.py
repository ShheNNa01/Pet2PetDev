from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, func
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import logging

from shared.database.models import (
    Post, GroupPost, Pet, User, Group,
    Follower, GroupMember, MediaFile,
    Reaction, Comment
)
from ..models.schemas import FeedType, ContentType, FeedFilters
from .ranking_service import RankingService

logger = logging.getLogger(__name__)

class AggregatorService:
    @staticmethod
    async def aggregate_content(
        db: Session,
        user_id: int,
        filters: FeedFilters,
        page: int = 1,
        page_size: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Agrega contenido de diferentes fuentes según los filtros
        y lo ordena por relevancia
        """
        try:
            aggregated_content = []

            # 1. Recolectar contenido según el tipo de feed
            if filters.feed_type == FeedType.FOLLOWING:
                content = await AggregatorService._aggregate_following_content(
                    db, user_id, filters
                )
            elif filters.feed_type == FeedType.GROUPS:
                content = await AggregatorService._aggregate_groups_content(
                    db, user_id, filters
                )
            elif filters.feed_type == FeedType.TRENDING:
                content = await AggregatorService._aggregate_trending_content(
                    db, user_id, filters
                )
            else:
                content = await AggregatorService._aggregate_mixed_content(
                    db, user_id, filters
                )

            # 2. Filtrar contenido según preferencias
            filtered_content = await AggregatorService._apply_filters(
                content, filters
            )

            # 3. Ordenar por relevancia usando RankingService
            ranked_content = await RankingService.rank_feed_items(
                db, filtered_content, user_id
            )

            # 4. Aplicar paginación
            start_idx = (page - 1) * page_size
            end_idx = start_idx + page_size
            paginated_content = ranked_content[start_idx:end_idx]

            return paginated_content

        except Exception as e:
            logger.error(f"Error aggregating content: {str(e)}")
            return []

    @staticmethod
    async def _aggregate_following_content(
        db: Session,
        user_id: int,
        filters: FeedFilters
    ) -> List[Dict[str, Any]]:
        """Recolecta contenido de mascotas seguidas"""
        try:
            # Obtener IDs de mascotas seguidas
            user_pets = db.query(Pet.pet_id).filter(Pet.user_id == user_id).all()
            user_pet_ids = [pet_id for (pet_id,) in user_pets]

            followed_pets = db.query(Follower.followed_pet_id).filter(
                Follower.follower_pet_id.in_(user_pet_ids)
            ).all()
            followed_pet_ids = [pet_id for (pet_id,) in followed_pets]

            # Obtener posts
            query = db.query(Post).filter(Post.pet_id.in_(followed_pet_ids))

            # Aplicar filtros temporales
            if filters.date_from:
                query = query.filter(Post.created_at >= filters.date_from)
            if filters.date_to:
                query = query.filter(Post.created_at <= filters.date_to)

            posts = query.order_by(desc(Post.created_at)).all()

            # Obtener estadísticas y media para cada post
            result = []
            for post in posts:
                # Contar reacciones y comentarios
                reactions_count = db.query(func.count(Reaction.reaction_id))\
                    .filter(Reaction.post_id == post.post_id)\
                    .scalar()
                    
                comments_count = db.query(func.count(Comment.comment_id))\
                    .filter(Comment.post_id == post.post_id)\
                    .scalar()

                # Obtener archivos multimedia
                media_files = db.query(MediaFile)\
                    .filter(MediaFile.post_id == post.post_id)\
                    .all()

                # Crear objeto de post enriquecido
                post_data = {
                    "id": post.post_id,
                    "type": "post",
                    "content": post.content,
                    "created_at": post.created_at,
                    "user_id": post.user_id,
                    "pet_id": post.pet_id,
                    "location": post.location,
                    "stats": {
                        "reactions_count": reactions_count,
                        "comments_count": comments_count
                    },
                    "media": [
                        {
                            "id": media.media_id,
                            "url": media.media_url,
                            "type": media.media_type
                        } for media in media_files
                    ],
                    "author": {
                        "user_id": post.user.user_id,
                        "user_name": f"{post.user.user_name} {post.user.user_last_name}",
                        "profile_picture": post.user.profile_picture
                    } if post.user else None,
                    "pet": {
                        "pet_id": post.pet.pet_id,
                        "name": post.pet.name,
                        "pet_picture": post.pet.pet_picture,
                        "breed_name": post.pet.breed.breed_name if post.pet.breed else None
                    } if post.pet else None
                }

                # Verificar si hay tags en el contenido
                if post.content:
                    # Extraer hashtags del contenido (implementación básica)
                    words = post.content.split()
                    tags = [word[1:] for word in words if word.startswith('#')]
                    if tags:
                        post_data["tags"] = tags

                result.append(post_data)

            return result

        except Exception as e:
            logger.error(f"Error aggregating following content: {str(e)}")
            return []
    
    @staticmethod
    async def _aggregate_groups_content(
        db: Session,
        user_id: int,
        filters: FeedFilters
    ) -> List[Dict[str, Any]]:
        """Recolecta contenido de grupos"""
        try:
            # Obtener grupos del usuario
            user_groups = db.query(GroupMember.group_id).filter(
                GroupMember.user_id == user_id
            ).all()
            group_ids = [group_id for (group_id,) in user_groups]

            # Obtener posts de grupos
            query = db.query(GroupPost).filter(GroupPost.group_id.in_(group_ids))

            if filters.date_from:
                query = query.filter(GroupPost.created_at >= filters.date_from)
            if filters.date_to:
                query = query.filter(GroupPost.created_at <= filters.date_to)

            group_posts = query.order_by(desc(GroupPost.created_at)).all()

            return [
                {
                    "id": post.group_post_id,
                    "type": "group_post",
                    "content": post.content,
                    "created_at": post.created_at,
                    "user_id": post.user_id,
                    "pet_id": post.pet_id,
                    "group_id": post.group_id,
                    "media": [
                        {
                            "id": media.media_id,
                            "url": media.media_url,
                            "type": media.media_type
                        } for media in post.media_files
                    ] if hasattr(post, 'media_files') else []
                } for post in group_posts
            ]

        except Exception as e:
            logger.error(f"Error aggregating group content: {str(e)}")
            return []

    @staticmethod
    async def _aggregate_trending_content(
        db: Session,
        user_id: int,
        filters: FeedFilters
    ) -> List[Dict[str, Any]]:
        """Recolecta contenido trending basado en interacciones"""
        try:
            # Subquery para calcular score de trending
            trending_score = db.query(
                Post.post_id,
                (
                    func.count(Reaction.reaction_id) * 1.0 +
                    func.count(Comment.comment_id) * 2.0
                ).label('score')
            ).outerjoin(Reaction).outerjoin(Comment)\
            .group_by(Post.post_id)\
            .subquery()

            # Obtener posts con mayor interacción
            query = db.query(Post).join(
                trending_score,
                Post.post_id == trending_score.c.post_id
            )

            # Filtrar por tiempo (últimas 24 horas por defecto)
            time_limit = filters.date_from or (datetime.utcnow() - timedelta(days=1))
            query = query.filter(Post.created_at >= time_limit)

            trending_posts = query.order_by(
                desc(trending_score.c.score),
                desc(Post.created_at)
            ).all()

            return [
                {
                    "id": post.post_id,
                    "type": "post",
                    "content": post.content,
                    "created_at": post.created_at,
                    "user_id": post.user_id,
                    "pet_id": post.pet_id,
                    "trending_score": getattr(post, 'score', 0.0),
                    "media": [
                        {
                            "id": media.media_id,
                            "url": media.media_url,
                            "type": media.media_type
                        } for media in post.media_files
                    ] if hasattr(post, 'media_files') else []
                } for post in trending_posts
            ]

        except Exception as e:
            logger.error(f"Error aggregating trending content: {str(e)}")
            return []

    @staticmethod
    async def _aggregate_mixed_content(
        db: Session,
        user_id: int,
        filters: FeedFilters
    ) -> List[Dict[str, Any]]:
        """Recolecta contenido mixto de todas las fuentes"""
        try:
            mixed_content = []

            # 1. Obtener posts regulares
            regular_posts = await AggregatorService._get_regular_posts(db, filters)
            mixed_content.extend(regular_posts)

            # 2. Obtener posts de grupos
            group_posts = await AggregatorService._get_public_group_posts(db, filters)
            mixed_content.extend(group_posts)

            # 3. Ordenar por fecha
            mixed_content.sort(key=lambda x: x["created_at"], reverse=True)

            return mixed_content

        except Exception as e:
            logger.error(f"Error aggregating mixed content: {str(e)}")
            return []

    @staticmethod
    async def _get_regular_posts(
        db: Session,
        filters: FeedFilters
    ) -> List[Dict[str, Any]]:
        """Obtener posts regulares"""
        try:
            query = db.query(Post)

            if filters.date_from:
                query = query.filter(Post.created_at >= filters.date_from)
            if filters.date_to:
                query = query.filter(Post.created_at <= filters.date_to)

            posts = query.order_by(desc(Post.created_at)).all()

            return [
                {
                    "id": post.post_id,
                    "type": "post",
                    "content": post.content,
                    "created_at": post.created_at,
                    "user_id": post.user_id,
                    "pet_id": post.pet_id,
                    "media": [
                        {
                            "id": media.media_id,
                            "url": media.media_url,
                            "type": media.media_type
                        } for media in post.media_files
                    ] if hasattr(post, 'media_files') else []
                } for post in posts
            ]

        except Exception as e:
            logger.error(f"Error getting regular posts: {str(e)}")
            return []

    @staticmethod
    async def _get_public_group_posts(
        db: Session,
        filters: FeedFilters
    ) -> List[Dict[str, Any]]:
        """Obtener posts de grupos públicos"""
        try:
            query = db.query(GroupPost).join(Group)\
                .filter(Group.privacy == False)

            if filters.date_from:
                query = query.filter(GroupPost.created_at >= filters.date_from)
            if filters.date_to:
                query = query.filter(GroupPost.created_at <= filters.date_to)

            group_posts = query.order_by(desc(GroupPost.created_at)).all()

            return [
                {
                    "id": post.group_post_id,
                    "type": "group_post",
                    "content": post.content,
                    "created_at": post.created_at,
                    "user_id": post.user_id,
                    "pet_id": post.pet_id,
                    "group_id": post.group_id,
                    "media": [
                        {
                            "id": media.media_id,
                            "url": media.media_url,
                            "type": media.media_type
                        } for media in post.media_files
                    ] if hasattr(post, 'media_files') else []
                } for post in group_posts
            ]

        except Exception as e:
            logger.error(f"Error getting public group posts: {str(e)}")
            return []

    @staticmethod
    async def _apply_filters(
        content: List[Dict[str, Any]],
        filters: FeedFilters
    ) -> List[Dict[str, Any]]:
        """Aplica filtros adicionales al contenido"""
        try:
            filtered_content = content

            # Filtrar por tipo de contenido
            if filters.content_types:
                filtered_content = [
                    item for item in filtered_content
                    if item["type"] in filters.content_types
                ]

            # Filtrar por mascota
            if filters.pet_id:
                filtered_content = [
                    item for item in filtered_content
                    if item.get("pet_id") == filters.pet_id
                ]

            # Filtrar por grupo
            if filters.group_id:
                filtered_content = [
                    item for item in filtered_content
                    if item.get("group_id") == filters.group_id
                ]

            # Filtrar por ubicación
            if filters.location:
                filtered_content = [
                    item for item in filtered_content
                    if filters.location.lower() in str(item.get("location", "")).lower()
                ]

            # Filtrar por tags
            if filters.tags:
                filtered_content = [
                    item for item in filtered_content
                    if any(tag in item.get("tags", []) for tag in filters.tags)
                ]

            return filtered_content

        except Exception as e:
            logger.error(f"Error applying filters: {str(e)}")
            return content  # Retornar contenido sin filtrar en caso de error