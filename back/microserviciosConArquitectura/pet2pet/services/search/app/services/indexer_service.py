from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, func, desc
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import logging
from shared.database.models import (
    Follower, Pet, User, Post, Group, Comment,
    PetType, Breed, GroupMember, MediaFile
)

logger = logging.getLogger(__name__)

class IndexerService:
    @staticmethod
    async def index_new_content(db: Session, content_type: str, content_id: int) -> bool:
        """
        Indexar nuevo contenido cuando se crea
        """
        try:
            if content_type == "pet":
                await IndexerService._index_pet(db, content_id)
            elif content_type == "post":
                await IndexerService._index_post(db, content_id)
            elif content_type == "group":
                await IndexerService._index_group(db, content_id)
            elif content_type == "user":
                await IndexerService._index_user(db, content_id)
            
            return True
        except Exception as e:
            logger.error(f"Error indexing {content_type} {content_id}: {str(e)}")
            return False

    @staticmethod
    async def update_index(db: Session, content_type: str, content_id: int) -> bool:
        """
        Actualizar índice cuando el contenido se modifica
        """
        try:
            if content_type == "pet":
                await IndexerService._update_pet_index(db, content_id)
            elif content_type == "post":
                await IndexerService._update_post_index(db, content_id)
            elif content_type == "group":
                await IndexerService._update_group_index(db, content_id)
            elif content_type == "user":
                await IndexerService._update_user_index(db, content_id)
            
            return True
        except Exception as e:
            logger.error(f"Error updating index for {content_type} {content_id}: {str(e)}")
            return False

    @staticmethod
    async def remove_from_index(db: Session, content_type: str, content_id: int) -> bool:
        """
        Eliminar contenido del índice
        """
        try:
            if content_type == "pet":
                await IndexerService._remove_pet_from_index(db, content_id)
            elif content_type == "post":
                await IndexerService._remove_post_from_index(db, content_id)
            elif content_type == "group":
                await IndexerService._remove_group_from_index(db, content_id)
            elif content_type == "user":
                await IndexerService._remove_user_from_index(db, content_id)
            
            return True
        except Exception as e:
            logger.error(f"Error removing {content_type} {content_id} from index: {str(e)}")
            return False

    @staticmethod
    async def reindex_all(db: Session) -> Dict[str, Any]:
        """
        Reindexar todo el contenido
        """
        results = {
            "pets": 0,
            "users": 0,
            "posts": 0,
            "groups": 0,
            "errors": []
        }

        try:
            # Reindexar mascotas
            pets = db.query(Pet).filter(Pet.status == True).all()
            for pet in pets:
                try:
                    await IndexerService._index_pet(db, pet.pet_id)
                    results["pets"] += 1
                except Exception as e:
                    results["errors"].append(f"Error indexing pet {pet.pet_id}: {str(e)}")

            # Reindexar usuarios
            users = db.query(User).filter(User.status == True).all()
            for user in users:
                try:
                    await IndexerService._index_user(db, user.user_id)
                    results["users"] += 1
                except Exception as e:
                    results["errors"].append(f"Error indexing user {user.user_id}: {str(e)}")

            # Reindexar posts
            posts = db.query(Post).all()
            for post in posts:
                try:
                    await IndexerService._index_post(db, post.post_id)
                    results["posts"] += 1
                except Exception as e:
                    results["errors"].append(f"Error indexing post {post.post_id}: {str(e)}")

            # Reindexar grupos
            groups = db.query(Group).all()
            for group in groups:
                try:
                    await IndexerService._index_group(db, group.group_id)
                    results["groups"] += 1
                except Exception as e:
                    results["errors"].append(f"Error indexing group {group.group_id}: {str(e)}")

        except Exception as e:
            logger.error(f"Error during complete reindex: {str(e)}")
            results["errors"].append(f"General error: {str(e)}")

        return results

    @staticmethod
    async def calculate_content_score(
        db: Session,
        content_type: str,
        content_id: int
    ) -> float:
        """
        Calcular score para ranking de búsqueda
        """
        try:
            if content_type == "pet":
                return await IndexerService._calculate_pet_score(db, content_id)
            elif content_type == "post":
                return await IndexerService._calculate_post_score(db, content_id)
            elif content_type == "group":
                return await IndexerService._calculate_group_score(db, content_id)
            elif content_type == "user":
                return await IndexerService._calculate_user_score(db, content_id)
            
            return 0.0
        except Exception as e:
            logger.error(f"Error calculating score for {content_type} {content_id}: {str(e)}")
            return 0.0

    # Métodos privados para indexación específica
    @staticmethod
    async def _index_pet(db: Session, pet_id: int) -> None:
        """
        Indexar una mascota y su información relacionada
        En una implementación real, aquí se agregaría la información a un motor de búsqueda
        como Elasticsearch
        """
        pet = db.query(Pet).filter(Pet.pet_id == pet_id).first()
        if not pet:
            return

        # Aquí se construiría el documento para el índice
        document = {
            "id": pet.pet_id,
            "name": pet.name,
            "type": "pet",
            "breed": pet.breed.breed_name if pet.breed else None,
            "pet_type": pet.breed.pet_type.type_name if pet.breed and pet.breed.pet_type else None,
            "bio": pet.bio,
            "gender": pet.gender,
            "owner": {
                "id": pet.user_id,
                "name": f"{pet.user.user_name} {pet.user.user_last_name}"
            },
            "created_at": pet.created_at.isoformat(),
            "updated_at": pet.updated_at.isoformat(),
            "score": await IndexerService._calculate_pet_score(db, pet_id)
        }

        # Aquí se enviaría el documento al motor de búsqueda
        logger.info(f"Indexed pet {pet_id}: {document}")

    @staticmethod
    async def _calculate_pet_score(db: Session, pet_id: int) -> float:
        """
        Calcular score de una mascota basado en varios factores
        """
        score = 1.0
        try:
            pet = db.query(Pet).filter(Pet.pet_id == pet_id).first()
            if not pet:
                return 0.0

            # Factor: completitud del perfil
            profile_completeness = 0.0
            if pet.name:
                profile_completeness += 0.2
            if pet.breed_id:
                profile_completeness += 0.2
            if pet.birthdate:
                profile_completeness += 0.2
            if pet.gender:
                profile_completeness += 0.2
            if pet.bio:
                profile_completeness += 0.2

            # Factor: actividad social
            followers_count = db.query(func.count(Follower.follower_id))\
                .filter(Follower.followed_pet_id == pet_id)\
                .scalar()
            
            # Factor: actividad en posts
            posts_count = db.query(func.count(Post.post_id))\
                .filter(Post.pet_id == pet_id)\
                .scalar()

            # Factor: actualización reciente
            days_since_update = (datetime.utcnow() - pet.updated_at).days
            recency_factor = 1.0 if days_since_update < 30 else (1.0 / (days_since_update / 30))

            # Combinar factores
            score = (
                (profile_completeness * 0.3) +
                (min(followers_count / 100, 1.0) * 0.3) +
                (min(posts_count / 50, 1.0) * 0.2) +
                (recency_factor * 0.2)
            )

        except Exception as e:
            logger.error(f"Error calculating pet score: {str(e)}")
            return 1.0

        return max(min(score, 1.0), 0.1)  # Normalizar entre 0.1 y 1.0

    
    # _index_user, _index_post, _index_group
    # _calculate_user_score, _calculate_post_score, _calculate_group_score
    # _update_*_index methods
    # _remove_*_from_index methods