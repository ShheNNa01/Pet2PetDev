from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, and_, or_
from datetime import datetime
from typing import List, Optional

from shared.database.models import Post, User, Pet, Comment, Reaction
from services.posts.app.models.schemas import PostCreate, PostUpdate, PostFilter, CommentCreate, ReactionCreate
from services.notifications.app.services.notification_service import NotificationService
from services.notifications.app.models.schemas import NotificationType

class PostService:
    @staticmethod
    async def create_post(db: Session, user_id: int, post_data: PostCreate) -> Post:
        # Verificar que la mascota existe y pertenece al usuario
        pet = db.query(Pet).filter(
            Pet.pet_id == post_data.pet_id,
            Pet.user_id == user_id
        ).first()
        
        if not pet:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pet not found or doesn't belong to user"
            )

        # Crear el post
        db_post = Post(
            user_id=user_id,
            content=post_data.content,
            location=post_data.location,
            pet_id=post_data.pet_id
        )

        try:
            db.add(db_post)
            db.commit()
            db.refresh(db_post)
            return db_post
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating post: {str(e)}"
            )

    @staticmethod
    async def create_comment(db: Session, user_id: int, post_id: int, comment_data: CommentCreate) -> Comment:
        try:
            # Verificar que el post existe
            post = db.query(Post).filter(Post.post_id == post_id).first()
            if not post:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Post not found"
                )

            # Crear el comentario
            db_comment = Comment(
                post_id=post_id,
                user_id=user_id,
                pet_id=comment_data.pet_id,
                comment=comment_data.comment
            )

            db.add(db_comment)

            # Si el comentario no es del dueño del post, crear notificación
            if post.user_id != user_id:
                # Obtener información de las mascotas
                commenter_pet = db.query(Pet).filter(Pet.pet_id == comment_data.pet_id).first()
                post_pet = db.query(Pet).filter(Pet.pet_id == post.pet_id).first()

                await NotificationService.create_notification_for_event(
                    db=db,
                    event_type=NotificationType.NEW_COMMENT,
                    user_id=post.user_id,
                    related_id=post_id,
                    custom_message=f"{commenter_pet.name} ha comentado en la publicación de {post_pet.name}"
                )

            db.commit()
            db.refresh(db_comment)
            return db_comment

        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating comment: {str(e)}"
            )

    @staticmethod
    async def create_reaction(db: Session, user_id: int, post_id: int, reaction_data: ReactionCreate) -> Reaction:
        try:
            # Verificar que el post existe
            post = db.query(Post).filter(Post.post_id == post_id).first()
            if not post:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Post not found"
                )

            # Verificar si ya existe una reacción
            existing_reaction = db.query(Reaction).filter(
                Reaction.post_id == post_id,
                Reaction.user_id == user_id,
                Reaction.pet_id == reaction_data.pet_id
            ).first()

            if existing_reaction:
                # Actualizar tipo de reacción si es diferente
                if existing_reaction.reaction_type != reaction_data.reaction_type:
                    existing_reaction.reaction_type = reaction_data.reaction_type
                    db.commit()
                return existing_reaction

            # Crear nueva reacción
            db_reaction = Reaction(
                post_id=post_id,
                user_id=user_id,
                pet_id=reaction_data.pet_id,
                reaction_type=reaction_data.reaction_type
            )

            db.add(db_reaction)

            # Si la reacción no es del dueño del post, crear notificación
            if post.user_id != user_id:
                # Obtener información de las mascotas
                reactor_pet = db.query(Pet).filter(Pet.pet_id == reaction_data.pet_id).first()
                post_pet = db.query(Pet).filter(Pet.pet_id == post.pet_id).first()

                await NotificationService.create_notification_for_event(
                    db=db,
                    event_type=NotificationType.NEW_REACTION,
                    user_id=post.user_id,
                    related_id=post_id,
                    custom_message=f"A {reactor_pet.name} le ha gustado la publicación de {post_pet.name}"
                )

            db.commit()
            db.refresh(db_reaction)
            return db_reaction

        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating reaction: {str(e)}"
            )

    @staticmethod
    async def get_posts(
        db: Session,
        skip: int = 0,
        limit: int = 10,
        filters: Optional[PostFilter] = None
    ) -> List[dict]:
        try:
            # Construir query base
            query = db.query(Post)
            
            # Aplicar filtros si existen
            if filters:
                if filters.pet_id:
                    query = query.filter(Post.pet_id == filters.pet_id)
                if filters.location:
                    query = query.filter(Post.location.ilike(f"%{filters.location}%"))
                if filters.from_date:
                    query = query.filter(Post.created_at >= filters.from_date)
                if filters.to_date:
                    query = query.filter(Post.created_at <= filters.to_date)

            # Obtener posts con todas las relaciones necesarias
            query = query.options(
                joinedload(Post.comments),
                joinedload(Post.reactions),
                joinedload(Post.media_files),
                joinedload(Post.pet)
            )

            # Ejecutar query con paginación
            posts = query.order_by(Post.created_at.desc()).offset(skip).limit(limit).all()

            # Formatear respuesta
            result = []
            for post in posts:
                media_urls = [media.media_url for media in post.media_files] if post.media_files else []
                
                post_dict = {
                    "post_id": post.post_id,
                    "content": post.content or "",
                    "location": post.location or "",
                    "pet_id": post.pet_id,
                    "user_id": post.pet.user_id if post.pet else None,
                    "created_at": post.created_at,
                    "updated_at": post.updated_at,
                    "media_urls": media_urls,
                    "comments_count": len(post.comments) if post.comments else 0,
                    "reactions_count": len(post.reactions) if post.reactions else 0,
                    "comments": []
                }

                # Añadir comentarios si existen
                if post.comments:
                    for comment in post.comments:
                        comment_dict = {
                            "comment_id": comment.comment_id,
                            "comment": comment.comment,
                            "post_id": comment.post_id,
                            "user_id": comment.user_id,
                            "pet_id": comment.pet_id,
                            "created_at": comment.created_at,
                            "updated_at": comment.updated_at,
                            "media_url": next((media.media_url for media in comment.media_files), None) if comment.media_files else None
                        }
                        post_dict["comments"].append(comment_dict)

                result.append(post_dict)

            return result

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error getting posts: {str(e)}"
            )

    @staticmethod
    async def get_post(db: Session, post_id: int) -> dict:
        post = db.query(Post).filter(Post.post_id == post_id).first()
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found"
            )
        
        return {
            "post_id": post.post_id,
            "content": post.content or "",
            "location": post.location or "",
            "pet_id": post.pet_id,
            "user_id": post.pet.user_id if post.pet else None,
            "created_at": post.created_at,
            "updated_at": post.updated_at,
            "media_urls": [media.media_url for media in post.media_files] if post.media_files else [],
            "comments_count": len(post.comments) if post.comments else 0,
            "reactions_count": len(post.reactions) if post.reactions else 0,
            "comments": [
                {
                    "comment_id": comment.comment_id,
                    "comment": comment.comment,
                    "post_id": comment.post_id,
                    "user_id": comment.user_id,
                    "pet_id": comment.pet_id,
                    "created_at": comment.created_at,
                    "updated_at": comment.updated_at,
                    "media_url": next((media.media_url for media in comment.media_files), None) if comment.media_files else None
                }
                for comment in post.comments
            ] if post.comments else []
        }

    @staticmethod
    async def update_post(
        db: Session,
        user_id: int,
        post_id: int,
        post_data: PostUpdate
    ) -> Post:
        post = db.query(Post).filter(
            Post.post_id == post_id,
            Post.user_id == user_id
        ).first()

        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found or not authorized"
            )

        # Actualizar campos
        for field, value in post_data.dict(exclude_unset=True).items():
            setattr(post, field, value)

        post.updated_at = datetime.utcnow()

        try:
            db.commit()
            db.refresh(post)
            return post
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error updating post: {str(e)}"
            )

    @staticmethod
    async def delete_post(db: Session, user_id: int, post_id: int) -> None:
        post = db.query(Post).filter(
            Post.post_id == post_id,
            Post.user_id == user_id
        ).first()

        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found or not authorized"
            )

        try:
            db.delete(post)
            db.commit()
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error deleting post: {str(e)}"
            )

    @staticmethod
    async def delete_comment(db: Session, user_id: int, comment_id: int) -> None:
        comment = db.query(Comment).filter(
            Comment.comment_id == comment_id,
            Comment.user_id == user_id
        ).first()

        if not comment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Comment not found or not authorized"
            )

        try:
            db.delete(comment)
            db.commit()
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error deleting comment: {str(e)}"
            )

    @staticmethod
    async def delete_reaction(db: Session, user_id: int, reaction_id: int) -> None:
        reaction = db.query(Reaction).filter(
            Reaction.reaction_id == reaction_id,
            Reaction.user_id == user_id
        ).first()

        if not reaction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Reaction not found or not authorized"
            )

        try:
            db.delete(reaction)
            db.commit()
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error deleting reaction: {str(e)}"
            )