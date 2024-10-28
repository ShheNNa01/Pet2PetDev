from sqlalchemy.orm import Session
from sqlalchemy import func, case, desc
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import math
import logging

from shared.database.models import (
    MediaFile, Post, GroupPost, Pet, User, Group,
    Reaction, Comment, Follower, GroupMember
)

logger = logging.getLogger(__name__)

class RankingService:
    @staticmethod
    async def calculate_post_score(
        db: Session,
        post_id: int,
        user_id: int,
        post_type: str = "post"
    ) -> float:
        """
        Calcula el score de relevancia para un post
        Factores considerados:
        - Tiempo desde la publicación
        - Interacciones (likes, comentarios)
        - Relevancia del autor
        - Afinidad con el usuario
        - Calidad del contenido
        """
        try:
            # Obtener el post y sus estadísticas
            if post_type == "post":
                post = db.query(Post).filter(Post.post_id == post_id).first()
                if not post:
                    return 0.0
            else:
                post = db.query(GroupPost).filter(GroupPost.group_post_id == post_id).first()
                if not post:
                    return 0.0

            # 1. Factor de tiempo (decae logarítmicamente)
            time_diff = datetime.utcnow() - post.created_at
            time_factor = 1.0 / (1.0 + math.log(1 + time_diff.total_seconds() / 3600))  # Decay por hora

            # 2. Factor de interacciones
            engagement_score = await RankingService._calculate_engagement_score(db, post_id, post_type)
            
            # 3. Factor de relevancia del autor
            author_score = await RankingService._calculate_author_relevance(db, post.user_id)
            
            # 4. Factor de afinidad con el usuario
            affinity_score = await RankingService._calculate_user_affinity(
                db, user_id, post.user_id, post.pet_id
            )
            
            # 5. Factor de calidad del contenido
            content_score = await RankingService._calculate_content_quality(db, post)

            # Combinar factores con pesos
            final_score = (
                time_factor * 0.3 +
                engagement_score * 0.25 +
                author_score * 0.15 +
                affinity_score * 0.2 +
                content_score * 0.1
            )

            return min(max(final_score, 0.0), 1.0)  # Normalizar entre 0 y 1

        except Exception as e:
            logger.error(f"Error calculating post score: {str(e)}")
            return 0.0

    @staticmethod
    async def rank_feed_items(
        db: Session,
        items: List[Dict[str, Any]],
        user_id: int
    ) -> List[Dict[str, Any]]:
        """
        Ordena los items del feed por relevancia
        """
        try:
            scored_items = []
            for item in items:
                score = await RankingService.calculate_post_score(
                    db,
                    item['id'],
                    user_id,
                    item['type']
                )
                scored_items.append((item, score))

            # Ordenar por score y retornar solo los items
            return [
                item for item, score in sorted(
                    scored_items,
                    key=lambda x: x[1],
                    reverse=True
                )
            ]

        except Exception as e:
            logger.error(f"Error ranking feed items: {str(e)}")
            return items  # Retornar items sin ordenar en caso de error

    @staticmethod
    async def _calculate_engagement_score(
        db: Session,
        post_id: int,
        post_type: str = "post"
    ) -> float:
        """
        Calcula el score basado en interacciones
        """
        try:
            # Contar likes y comentarios
            if post_type == "post":
                likes = db.query(func.count(Reaction.reaction_id))\
                    .filter(Reaction.post_id == post_id).scalar()
                comments = db.query(func.count(Comment.comment_id))\
                    .filter(Comment.post_id == post_id).scalar()
            else:
                likes = db.query(func.count(Reaction.reaction_id))\
                    .filter(Reaction.group_post_id == post_id).scalar()
                comments = db.query(func.count(Comment.comment_id))\
                    .filter(Comment.group_post_id == post_id).scalar()

            # Normalizar y combinar (los comentarios valen más que los likes)
            engagement_score = (likes * 1.0 + comments * 2.0) / 100.0
            return min(engagement_score, 1.0)

        except Exception as e:
            logger.error(f"Error calculating engagement score: {str(e)}")
            return 0.0

    @staticmethod
    async def _calculate_author_relevance(
        db: Session,
        author_id: int
    ) -> float:
        """
        Calcula la relevancia del autor basada en su actividad y seguidores
        """
        try:
            # Obtener estadísticas del autor
            author_pets = db.query(Pet).filter(Pet.user_id == author_id).all()
            if not author_pets:
                return 0.0

            total_followers = 0
            total_posts = 0
            for pet in author_pets:
                # Contar seguidores
                followers = db.query(func.count(Follower.follower_id))\
                    .filter(Follower.followed_pet_id == pet.pet_id).scalar()
                total_followers += followers

                # Contar posts
                posts = db.query(func.count(Post.post_id))\
                    .filter(Post.pet_id == pet.pet_id).scalar()
                total_posts += posts

            # Calcular score combinado
            follower_score = min(total_followers / 1000.0, 1.0)  # Normalizar a 1000 seguidores
            post_score = min(total_posts / 100.0, 1.0)  # Normalizar a 100 posts

            return (follower_score * 0.7 + post_score * 0.3)

        except Exception as e:
            logger.error(f"Error calculating author relevance: {str(e)}")
            return 0.0

    @staticmethod
    async def _calculate_user_affinity(
        db: Session,
        user_id: int,
        author_id: int,
        pet_id: Optional[int]
    ) -> float:
        """
        Calcula la afinidad entre el usuario y el autor/mascota
        """
        try:
            affinity_score = 0.0
            user_pets = db.query(Pet).filter(Pet.user_id == user_id).all()
            
            if not user_pets:
                return 0.0

            # Verificar si sigue a la mascota
            if pet_id:
                for user_pet in user_pets:
                    follows = db.query(Follower)\
                        .filter(
                            Follower.follower_pet_id == user_pet.pet_id,
                            Follower.followed_pet_id == pet_id
                        ).first()
                    if follows:
                        affinity_score += 0.5
                        break

            # Verificar interacciones previas
            last_month = datetime.utcnow() - timedelta(days=30)
            
            # Contar likes en posts del autor
            likes = db.query(func.count(Reaction.reaction_id))\
                .join(Post)\
                .filter(
                    Reaction.user_id == user_id,
                    Post.user_id == author_id,
                    Reaction.created_at >= last_month
                ).scalar()

            # Contar comentarios en posts del autor
            comments = db.query(func.count(Comment.comment_id))\
                .join(Post)\
                .filter(
                    Comment.user_id == user_id,
                    Post.user_id == author_id,
                    Comment.created_at >= last_month
                ).scalar()

            # Calcular score de interacciones
            interaction_score = min((likes + comments * 2) / 20.0, 0.5)
            affinity_score += interaction_score

            return min(affinity_score, 1.0)

        except Exception as e:
            logger.error(f"Error calculating user affinity: {str(e)}")
            return 0.0

    @staticmethod
    async def _calculate_content_quality(
        db: Session,
        post: Any
    ) -> float:
        """
        Calcula la calidad del contenido basada en varios factores
        """
        try:
            quality_score = 0.0

            # 1. Longitud del contenido
            if hasattr(post, 'content') and post.content:
                content_length = len(post.content)
                if content_length > 50:
                    quality_score += 0.2
                if content_length > 200:
                    quality_score += 0.2

            # 2. Presencia de media
            media_count = db.query(func.count(MediaFile.media_id))\
                .filter(
                    MediaFile.post_id == post.post_id if isinstance(post, Post)
                    else MediaFile.group_post_id == post.group_post_id
                ).scalar()
            
            if media_count > 0:
                quality_score += 0.3

            # 3. Presencia de ubicación
            if hasattr(post, 'location') and post.location:
                quality_score += 0.2

            # 4. Ratio de interacciones positivas
            total_reactions = db.query(func.count(Reaction.reaction_id))\
                .filter(
                    Reaction.post_id == post.post_id if isinstance(post, Post)
                    else Reaction.group_post_id == post.group_post_id
                ).scalar()
            
            if total_reactions > 0:
                positive_ratio = total_reactions / (total_reactions + 1)  # Evitar división por cero
                quality_score += 0.1 * positive_ratio

            return quality_score

        except Exception as e:
            logger.error(f"Error calculating content quality: {str(e)}")
            return 0.0

    @staticmethod
    async def boost_content(
        content_id: int,
        boost_factor: float,
        boost_duration: timedelta
    ) -> bool:
        """
        Aplicar boost temporal a contenido específico
        Útil para contenido promocionado o destacado
        """
        try:
            # Implementar lógica de boost
            return True
        except Exception as e:
            logger.error(f"Error applying boost: {str(e)}")
            return False