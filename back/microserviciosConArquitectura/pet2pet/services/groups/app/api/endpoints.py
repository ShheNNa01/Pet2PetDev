from fastapi import APIRouter, Depends, HTTPException, status, Query, File, UploadFile
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from shared.database.session import get_db
from shared.database.models import User
from services.auth.app.api.dependencies import get_current_active_user
from services.groups.app.models.schemas import (
    GroupCreate, GroupUpdate, GroupResponse,
    GroupPostCreate, GroupPostResponse,
    GroupMemberCreate, GroupMemberResponse,
    GroupCommentCreate, GroupCommentResponse, MediaFileResponse
)
from services.groups.app.services.group_service import GroupService

router = APIRouter()

# Grupos
@router.post("/", response_model=GroupResponse, status_code=status.HTTP_201_CREATED)
async def create_group(
    group_data: GroupCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Crear un nuevo grupo.
    El usuario que lo crea se convierte automáticamente en propietario y administrador.
    """
    return await GroupService.create_group(db, current_user.user_id, group_data)

@router.get("/", response_model=List[GroupResponse])
async def get_groups(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    search: Optional[str] = None,
    privacy: Optional[bool] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Obtener lista de grupos.
    Se pueden filtrar por privacidad y buscar por nombre.
    """
    return await GroupService.get_groups(
        db, 
        current_user.user_id,
        skip=skip,
        limit=limit,
        search=search,
        privacy=privacy
    )

@router.get("/my-groups", response_model=List[GroupResponse])
async def get_my_groups(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    admin_only: bool = False,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Obtener grupos del usuario actual.
    Puede filtrar solo los grupos donde es administrador.
    """
    return await GroupService.get_user_groups(
        db,
        current_user.user_id,
        skip=skip,
        limit=limit,
        admin_only=admin_only
    )

@router.get("/{group_id}", response_model=GroupResponse)
async def get_group(
    group_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Obtener detalles de un grupo específico.
    """
    return await GroupService.get_group(db, group_id, current_user.user_id)

@router.put("/{group_id}", response_model=GroupResponse)
async def update_group(
    group_id: int,
    group_data: GroupUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Actualizar información del grupo.
    Solo permitido para propietarios y administradores.
    """
    return await GroupService.update_group(
        db,
        group_id,
        current_user.user_id,
        group_data
    )

@router.post("/{group_id}/image", response_model=GroupResponse)
async def upload_group_image(
    group_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Subir o actualizar la imagen del grupo.
    Solo permitido para propietarios y administradores.
    """
    return await GroupService.upload_group_image(
        db,
        group_id,
        current_user.user_id,
        file
    )

# Miembros
@router.post("/{group_id}/join", response_model=GroupMemberResponse)
async def join_group(
    group_id: int,
    member_data: GroupMemberCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Unirse a un grupo.
    """
    return await GroupService.join_group(
        db,
        group_id,
        current_user.user_id,
        member_data
    )

@router.delete("/{group_id}/leave", status_code=status.HTTP_204_NO_CONTENT)
async def leave_group(
    group_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Abandonar un grupo.
    Los propietarios no pueden abandonar, deben transferir la propiedad primero.
    """
    await GroupService.leave_group(db, group_id, current_user.user_id)

@router.get("/{group_id}/members", response_model=List[GroupMemberResponse])
async def get_members(
    group_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    admin_only: bool = False,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Obtener lista de miembros del grupo.
    Puede filtrar solo administradores.
    """
    return await GroupService.get_members(
        db,
        group_id,
        current_user.user_id,
        skip=skip,
        limit=limit,
        admin_only=admin_only
    )

@router.post("/{group_id}/members/{user_id}/make-admin", response_model=GroupMemberResponse)
async def make_admin(
    group_id: int,
    user_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Convertir a un miembro en administrador.
    Solo permitido para propietarios y administradores.
    """
    return await GroupService.make_admin(
        db,
        group_id,
        current_user.user_id,
        user_id
    )

# Posts y Comentarios
@router.post("/{group_id}/posts", response_model=GroupPostResponse)
async def create_post(
    group_id: int,
    post_data: GroupPostCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Crear una publicación en el grupo.
    Solo miembros pueden publicar.
    """
    return await GroupService.create_post(
        db,
        group_id,
        current_user.user_id,
        post_data
    )

@router.get("/{group_id}/posts", response_model=List[GroupPostResponse])
async def get_posts(
    group_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Obtener publicaciones del grupo.
    """
    return await GroupService.get_posts(
        db,
        group_id,
        current_user.user_id,
        skip=skip,
        limit=limit
    )

@router.post("/{group_id}/posts/{post_id}/comments", response_model=GroupCommentResponse)
async def create_comment(
    group_id: int,
    post_id: int,
    comment_data: GroupCommentCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Comentar en una publicación del grupo.
    Solo miembros pueden comentar.
    """
    return await GroupService.create_comment(
        db,
        group_id,
        post_id,
        current_user.user_id,
        comment_data
    )

# Moderación
@router.post("/{group_id}/members/{user_id}/remove", status_code=status.HTTP_204_NO_CONTENT)
async def remove_member(
    group_id: int,
    user_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Remover a un miembro del grupo.
    Solo permitido para propietarios y administradores.
    """
    await GroupService.remove_member(
        db,
        group_id,
        current_user.user_id,
        user_id
    )

@router.delete("/{group_id}/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    group_id: int,
    post_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Eliminar una publicación.
    Solo permitido para el autor, propietarios y administradores.
    """
    await GroupService.delete_post(
        db,
        group_id,
        post_id,
        current_user.user_id
    )

@router.post("/{group_id}/posts/{post_id}/media", response_model=List[MediaFileResponse])
async def attach_media_to_post(
        group_id: int,
        post_id: int,
        files: List[UploadFile] = File(...),
        current_user: User = Depends(get_current_active_user),
        db: Session = Depends(get_db)
    ):
        """
        Attach media files to a group post.
        Only the post author can attach media.
        """
        return await GroupService.attach_media_to_post(
            db,
            group_id,
            post_id,
            current_user.user_id,
            files
        )

@router.post("/{group_id}/transfer-ownership/{new_owner_id}", response_model=GroupResponse)
async def transfer_group_ownership(
        group_id: int,
        new_owner_id: int,
        current_user: User = Depends(get_current_active_user),
        db: Session = Depends(get_db)
    ):
        """
        Transfer group ownership to another member.
        Only the current owner can transfer ownership.
        """
        return await GroupService.transfer_ownership(
            db,
            group_id,
            current_user.user_id,
            new_owner_id
        )

@router.get("/{group_id}/posts/{post_id}/comments", response_model=List[GroupCommentResponse])
async def get_post_comments(
        group_id: int,
        post_id: int,
        skip: int = Query(0, ge=0),
        limit: int = Query(20, ge=1, le=100),
        current_user: User = Depends(get_current_active_user),
        db: Session = Depends(get_db)
    ):
        """
        Get comments for a specific post.
        """
        return await GroupService.get_post_comments(
            db,
            group_id,
            post_id,
            current_user.user_id,
            skip,
            limit
        )

@router.delete("/{group_id}/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
        group_id: int,
        comment_id: int,
        current_user: User = Depends(get_current_active_user),
        db: Session = Depends(get_db)
    ):
        """
        Delete a comment.
        Can be deleted by comment author, group owner, or admins.
        """
        await GroupService.delete_comment(
            db,
            group_id,
            comment_id,
            current_user.user_id
        )