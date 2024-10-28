from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, desc, func
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
import time
import logging

from shared.database.models import (
    Post, GroupPost, Pet, Group, User, 
    Follower, GroupMember, MediaFile,
    Comment, Reaction
)
from ..models.schemas import (
    FeedType, ContentType, FeedItem, FeedResponse,
    FeedFilters, UserPreview, PetPreview, GroupPreview,
    MediaContent, FeedItemStats, FeedPreferences
)

logger = logging.getLogger(__name__)

class FeedService:
    @staticmethod
    async def get_feed(
        db: Session,
        user_id: int,
        filters: FeedFilters,
        page: int = 1,
        page_size: int = 20,
        preferences: Optional[FeedPreferences] = None
    ) -> FeedResponse:
        """Obtener feed personalizado según filtros y preferencias"""
        start_time = time.time()
        try:
            # Aplicar filtros según el tipo de feed
            if filters.feed_type == FeedType.FOLLOWING:
                items = await FeedService._get_following_feed(
                    db, user_id, filters, page, page_size
                )
            elif filters.feed_type == FeedType.GROUPS:
                items = await FeedService._get_groups_feed(
                    db, user_id, filters, page, page_size
                )
            elif filters.feed_type == FeedType.TRENDING:
                items = await FeedService._get_trending_feed(
                    db, user_id, filters, page, page_size
                )
            else:
                items = await FeedService._get_main_feed(
                    db, user_id, filters, page, page_size
                )

            # Enriquecer los items con información adicional
            enriched_items = []
            for item in items:
                try:
                    enriched_item = await FeedService._enrich_feed_item(db, item, user_id)
                    enriched_items.append(enriched_item)
                except Exception as e:
                    logger.error(f"Error enriching feed item: {str(e)}")
                    continue

            # Calcular estadísticas del feed
            total_items = await FeedService._get_total_items(db, user_id, filters)
            total_pages = -(-total_items // page_size)  # Redondeo hacia arriba
            has_more = page < total_pages
            
            # Generar cursor para paginación
            next_cursor = None
            if has_more and enriched_items:
                next_cursor = str(enriched_items[-1].created_at.timestamp())

            return FeedResponse(
                items=enriched_items,
                total_items=total_items,
                page=page,
                total_pages=total_pages,
                has_more=has_more,
                next_cursor=next_cursor,
                feed_type=filters.feed_type,
                processing_time=time.time() - start_time
            )

        except Exception as e:
            logger.error(f"Error getting feed: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error retrieving feed: {str(e)}"
            )

    @staticmethod
    async def _get_following_feed(
        db: Session,
        user_id: int,
        filters: FeedFilters,
        page: int,
        page_size: int
    ) -> List[Any]:
        """Obtener feed de mascotas seguidas"""
        try:
            # Obtener IDs de mascotas seguidas
            followed_pets = db.query(Follower.followed_pet_id).filter(
                Follower.follower_pet_id.in_(
                    db.query(Pet.pet_id).filter(Pet.user_id == user_id)
                )
            ).all()
            followed_pet_ids = [pet_id for (pet_id,) in followed_pets]

            # Obtener posts de mascotas seguidas
            query = db.query(Post).filter(
                Post.pet_id.in_(followed_pet_ids)
            )

            # Aplicar filtros adicionales
            if filters.date_from:
                query = query.filter(Post.created_at >= filters.date_from)
            if filters.date_to:
                query = query.filter(Post.created_at <= filters.date_to)

            # Ordenar y paginar
            return query.order_by(desc(Post.created_at))\
                .offset((page - 1) * page_size)\
                .limit(page_size)\
                .all()

        except Exception as e:
            logger.error(f"Error getting following feed: {str(e)}")
            raise

    @staticmethod
    async def _get_groups_feed(
        db: Session,
        user_id: int,
        filters: FeedFilters,
        page: int,
        page_size: int
    ) -> List[Any]:
        """Obtener feed de grupos"""
        try:
            # Obtener IDs de grupos del usuario
            user_groups = db.query(GroupMember.group_id).filter(
                GroupMember.user_id == user_id
            ).all()
            group_ids = [group_id for (group_id,) in user_groups]

            # Obtener posts de los grupos
            query = db.query(GroupPost).filter(
                GroupPost.group_id.in_(group_ids)
            )

            # Aplicar filtros adicionales
            if filters.date_from:
                query = query.filter(GroupPost.created_at >= filters.date_from)
            if filters.date_to:
                query = query.filter(GroupPost.created_at <= filters.date_to)

            # Ordenar y paginar
            return query.order_by(desc(GroupPost.created_at))\
                .offset((page - 1) * page_size)\
                .limit(page_size)\
                .all()

        except Exception as e:
            logger.error(f"Error getting groups feed: {str(e)}")
            raise

    @staticmethod
    async def _get_trending_feed(
        db: Session,
        user_id: int,
        filters: FeedFilters,
        page: int,
        page_size: int
    ) -> List[Any]:
        """Obtener feed de contenido trending"""
        try:
            # Subquery para contar interacciones
            interactions_count = db.query(
                Post.post_id,
                (func.count(Reaction.reaction_id) + func.count(Comment.comment_id) * 2).label('score')
            ).outerjoin(Reaction).outerjoin(Comment)\
            .group_by(Post.post_id)\
            .subquery()

            # Obtener posts populares
            query = db.query(Post).join(
                interactions_count,
                Post.post_id == interactions_count.c.post_id
            )

            # Filtrar por tiempo (últimas 24 horas por defecto)
            time_limit = filters.date_from or (datetime.utcnow() - timedelta(days=1))
            query = query.filter(Post.created_at >= time_limit)

            # Ordenar por score y fecha
            return query.order_by(
                desc(interactions_count.c.score),
                desc(Post.created_at)
            ).offset((page - 1) * page_size)\
            .limit(page_size)\
            .all()

        except Exception as e:
            logger.error(f"Error getting trending feed: {str(e)}")
            raise

    @staticmethod
    async def _get_main_feed(
        db: Session,
        user_id: int,
        filters: FeedFilters,
        page: int,
        page_size: int
    ) -> List[Any]:
        """Obtener feed principal mezclando diferentes fuentes"""
        try:
            # Combinar posts normales y posts de grupos
            posts_query = db.query(Post).filter(Post.user_id != user_id)
            group_posts_query = db.query(GroupPost).join(Group)\
                .filter(Group.privacy == False)  # Solo grupos públicos

            if filters.date_from:
                posts_query = posts_query.filter(Post.created_at >= filters.date_from)
                group_posts_query = group_posts_query.filter(
                    GroupPost.created_at >= filters.date_from
                )

            # Obtener y mezclar resultados
            posts = posts_query.order_by(desc(Post.created_at))\
                .limit(page_size).all()
            group_posts = group_posts_query.order_by(desc(GroupPost.created_at))\
                .limit(page_size).all()

            # Mezclar y ordenar por fecha
            combined_items = []
            combined_items.extend(posts)
            combined_items.extend(group_posts)
            
            combined_items.sort(
                key=lambda x: x.created_at,
                reverse=True
            )

            return combined_items[
                (page - 1) * page_size:
                page * page_size
            ]

        except Exception as e:
            logger.error(f"Error getting main feed: {str(e)}")
            raise

    @staticmethod
    async def _enrich_feed_item(
        db: Session,
        item: Any,
        user_id: int
    ) -> FeedItem:
        """Enriquecer item con información adicional"""
        try:
            # Determinar tipo de contenido
            if isinstance(item, Post):
                content_type = ContentType.POST
                content = {
                    "text": item.content,
                    "location": item.location
                }
                user = item.user
                pet = item.pet
                group = None
            elif isinstance(item, GroupPost):
                content_type = ContentType.GROUP_POST
                content = {
                    "text": item.content
                }
                user = item.user
                pet = item.pet
                group = item.group
            else:
                raise ValueError(f"Unknown item type: {type(item)}")

            # Obtener estadísticas
            likes_count = db.query(func.count(Reaction.reaction_id))\
                .filter(
                    Reaction.post_id == item.post_id if isinstance(item, Post)
                    else Reaction.group_post_id == item.group_post_id
                ).scalar()

            comments_count = db.query(func.count(Comment.comment_id))\
                .filter(
                    Comment.post_id == item.post_id if isinstance(item, Post)
                    else Comment.group_post_id == item.group_post_id
                ).scalar()

            # Verificar si el usuario actual dio like
            is_liked = db.query(Reaction)\
                .filter(
                    Reaction.user_id == user_id,
                    Reaction.post_id == item.post_id if isinstance(item, Post)
                    else Reaction.group_post_id == item.group_post_id
                ).first() is not None

            # Obtener archivos multimedia
            media_files = db.query(MediaFile)\
                .filter(
                    MediaFile.post_id == item.post_id if isinstance(item, Post)
                    else MediaFile.group_post_id == item.group_post_id
                ).all()

            return FeedItem(
                item_id=f"{content_type}_{item.post_id if isinstance(item, Post) else item.group_post_id}",
                content_type=content_type,
                created_at=item.created_at,
                relevance_score=1.0,  # Implementar scoring más sofisticado
                content=content,
                user=UserPreview(
                    user_id=user.user_id,
                    user_name=f"{user.user_name} {user.user_last_name}",
                    profile_picture=user.profile_picture
                ),
                pet=PetPreview(
                    pet_id=pet.pet_id,
                    name=pet.name,
                    pet_picture=pet.pet_picture,
                    breed_name=pet.breed.breed_name if pet and pet.breed else None
                ) if pet else None,
                group=GroupPreview(
                    group_id=group.group_id,
                    name_group=group.name_group,
                    group_picture=group.group_picture
                ) if group else None,
                media=[
                    MediaContent(
                        media_id=media.media_id,
                        media_url=media.media_url,
                        media_type=media.media_type,
                        thumbnail_url=None  # Implementar generación de thumbnails
                    ) for media in media_files
                ],
                stats=FeedItemStats(
                    likes_count=likes_count,
                    comments_count=comments_count,
                    shares_count=0  # Implementar conteo de shares
                ),
                is_liked=is_liked,
                is_shared=False,  # Implementar verificación de shares
                location=item.location if isinstance(item, Post) else None,
                tags=[]  # Implementar sistema de tags
            )

        except Exception as e:
            logger.error(f"Error enriching feed item: {str(e)}")
            raise

    @staticmethod
    async def _get_total_items(
        db: Session,
        user_id: int,
        filters: FeedFilters
    ) -> int:
        """Obtener total de items según los filtros"""
        try:
            if filters.feed_type == FeedType.FOLLOWING:
                return db.query(func.count(Post.post_id))\
                    .filter(Post.pet_id.in_(
                        db.query(Follower.followed_pet_id)
                        .filter(Follower.follower_pet_id.in_(
                            db.query(Pet.pet_id)
                            .filter(Pet.user_id == user_id)
                        ))
                    )).scalar()
            elif filters.feed_type == FeedType.GROUPS:
                return db.query(func.count(GroupPost.group_post_id))\
                    .filter(GroupPost.group_id.in_(
                        db.query(GroupMember.group_id)
                        .filter(GroupMember.user_id == user_id)
                    )).scalar()
            else:
                return db.query(func.count(Post.post_id)).scalar()

        except Exception as e:
            logger.error(f"Error getting total items: {str(e)}")
            raise