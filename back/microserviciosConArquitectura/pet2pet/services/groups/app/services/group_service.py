from fastapi import HTTPException, status, UploadFile
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, or_
from typing import List, Optional
from datetime import datetime
import os
import uuid

from shared.database.models import (
    Group, GroupMember, GroupPost, GroupComment,
    User, Pet, MediaFile
)
from services.notifications.app.services.notification_service import NotificationService
from services.notifications.app.models.schemas import NotificationType
from services.groups.app.models.schemas import (
    GroupCreate, GroupUpdate, GroupMemberCreate,
    GroupPostCreate, GroupCommentCreate
)

class GroupService:
    @staticmethod
    async def create_group(
        db: Session,
        owner_id: int,
        group_data: GroupCreate
    ) -> Group:
        """Create a new group"""
        try:
            db_group = Group(
                name_group=group_data.name_group,
                description=group_data.description,
                privacy=group_data.privacy,
                owner_id=owner_id
            )
            
            db.add(db_group)
            db.flush()  # Get the group_id before committing

            # Create initial membership for owner
            owner_member = GroupMember(
                group_id=db_group.group_id,
                user_id=owner_id,
                admin=True  # Owner is automatically admin
            )
            
            db.add(owner_member)
            db.commit()
            db.refresh(db_group)

            # Notificar al owner
            await NotificationService.create_notification_for_event(
                db=db,
                event_type=NotificationType.SYSTEM,
                user_id=owner_id,
                related_id=db_group.group_id,
                custom_message=f"Has creado el grupo: {group_data.name_group}",
                additional_data={"group_id": db_group.group_id, "group_name": group_data.name_group}
            )
            
            return db_group
            
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating group: {str(e)}"
            )

    @staticmethod
    async def get_group(
        db: Session,
        group_id: int,
        current_user_id: int
    ) -> Group:
        """Get group details with membership info"""
        group = db.query(Group).filter(Group.group_id == group_id).first()
        
        if not group:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Group not found"
            )

        # Check privacy and membership
        if group.privacy:
            membership = db.query(GroupMember).filter(
                GroupMember.group_id == group_id,
                GroupMember.user_id == current_user_id
            ).first()
            
            if not membership and group.owner_id != current_user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="This is a private group"
                )

        return group

    @staticmethod
    async def update_group(
        db: Session,
        group_id: int,
        current_user_id: int,
        group_data: GroupUpdate
    ) -> Group:
        """Update group details"""
        group = db.query(Group).filter(Group.group_id == group_id).first()
        
        if not group:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Group not found"
            )

        # Check if user is owner or admin
        if group.owner_id != current_user_id:
            admin = db.query(GroupMember).filter(
                GroupMember.group_id == group_id,
                GroupMember.user_id == current_user_id,
                GroupMember.admin == True
            ).first()
            
            if not admin:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Only owner and admins can update group"
                )

        # Update fields
        for field, value in group_data.model_dump(exclude_unset=True).items():
            setattr(group, field, value)

        try:
            db.commit()
            db.refresh(group)
            return group
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error updating group: {str(e)}"
            )

    @staticmethod
    async def join_group(
        db: Session,
        group_id: int,
        user_id: int,
        member_data: GroupMemberCreate
    ) -> GroupMember:
        """Join a group"""
        group = db.query(Group).filter(Group.group_id == group_id).first()
        
        if not group:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Group not found"
            )

        # Check if already a member
        existing_member = db.query(GroupMember).filter(
            GroupMember.group_id == group_id,
            GroupMember.user_id == user_id
        ).first()
        
        if existing_member:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Already a member of this group"
            )

        try:
            member = GroupMember(
                group_id=group_id,
                user_id=user_id,
                pet_id=member_data.pet_id,
                admin=False
            )
            
            db.add(member)
            
            # Notify group owner
            await NotificationService.create_notification_for_event(
                db=db,
                event_type=NotificationType.GROUP_MEMBER_JOINED,
                user_id=group.owner_id,
                related_id=group_id,
                additional_data={
                    "group_id": group_id,
                    "group_name": group.name_group,
                    "new_member_id": user_id
                }
            )
            
            db.commit()
            db.refresh(member)
            return member

        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error joining group: {str(e)}"
            )

    @staticmethod
    async def create_post(
        db: Session,
        group_id: int,
        user_id: int,
        post_data: GroupPostCreate
    ) -> GroupPost:
        """Create a post in a group"""
        # Check membership
        member = db.query(GroupMember).filter(
            GroupMember.group_id == group_id,
            GroupMember.user_id == user_id
        ).first()
        
        if not member:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Must be a member to post"
            )

        try:
            post = GroupPost(
                group_id=group_id,
                user_id=user_id,
                pet_id=member.pet_id,
                content=post_data.content
            )
            
            db.add(post)
            db.commit()
            db.refresh(post)

            members = db.query(GroupMember).filter(
                GroupMember.group_id == group_id,
                GroupMember.user_id != user_id  # No notificar al autor
            ).all()
            
            for member in members:
                await NotificationService.create_notification_for_event(
                    db=db,
                    event_type=NotificationType.GROUP_POST_NEW,
                    user_id=member.user_id,
                    related_id=post.group_post_id,
                    additional_data={
                        "group_id": group_id,
                        "post_id": post.group_post_id,
                        "author_id": user_id
                    }
                )

            return post

        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating post: {str(e)}"
            )

    @staticmethod
    async def get_groups(
        db: Session,
        current_user_id: int,
        skip: int = 0,
        limit: int = 10,
        search: Optional[str] = None,
        privacy: Optional[bool] = None
    ) -> List[Group]:
        """Get groups with filters"""
        try:
            query = db.query(Group)

            # Apply filters
            if search:
                query = query.filter(
                    or_(
                        Group.name_group.ilike(f"%{search}%"),
                        Group.description.ilike(f"%{search}%")
                    )
                )

            if privacy is not None:
                query = query.filter(Group.privacy == privacy)

            # For private groups, only show if user is member
            private_groups = query.filter(
                Group.privacy == True,
                Group.group_id.in_(
                    db.query(GroupMember.group_id).filter(
                        GroupMember.user_id == current_user_id
                    )
                )
            )

            # Public groups
            public_groups = query.filter(Group.privacy == False)

            # Combine results
            groups = private_groups.union(public_groups)\
                .order_by(desc(Group.created_at))\
                .offset(skip)\
                .limit(limit)\
                .all()

            return groups

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error retrieving groups: {str(e)}"
            )

    @staticmethod
    async def get_user_groups(
        db: Session,
        user_id: int,
        skip: int = 0,
        limit: int = 10,
        admin_only: bool = False
    ) -> List[Group]:
        """Get groups where user is member"""
        try:
            query = db.query(Group).join(GroupMember).filter(
                GroupMember.user_id == user_id
            )

            if admin_only:
                query = query.filter(GroupMember.admin == True)

            return query.order_by(desc(Group.created_at))\
                .offset(skip)\
                .limit(limit)\
                .all()

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error retrieving user groups: {str(e)}"
            )

    @staticmethod
    async def leave_group(
        db: Session,
        group_id: int,
        user_id: int
    ) -> None:
        """Leave a group"""
        try:
            group = db.query(Group).filter(Group.group_id == group_id).first()
            if not group:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Group not found"
                )

            # Owner can't leave
            if group.owner_id == user_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Owner cannot leave group. Transfer ownership first"
                )

            membership = db.query(GroupMember).filter(
                GroupMember.group_id == group_id,
                GroupMember.user_id == user_id
            ).first()

            if not membership:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Not a member of this group"
                )

            db.delete(membership)
            db.commit()

        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error leaving group: {str(e)}"
            )

    @staticmethod
    async def make_admin(
        db: Session,
        group_id: int,
        current_user_id: int,
        user_id: int
    ) -> GroupMember:
        """Make a member admin"""
        try:
            # Check if current user is owner or admin
            current_member = db.query(GroupMember).filter(
                GroupMember.group_id == group_id,
                GroupMember.user_id == current_user_id
            ).first()

            if not current_member or (not current_member.admin and current_user_id != db.query(Group.owner_id).filter(Group.group_id == group_id).scalar()):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Only owner and admins can manage admins"
                )

            # Update target member
            member = db.query(GroupMember).filter(
                GroupMember.group_id == group_id,
                GroupMember.user_id == user_id
            ).first()

            if not member:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User is not a member of this group"
                )

            member.admin = True
            db.commit()
            db.refresh(member)

            # Notify new admin
            await NotificationService.create_notification_for_event(
                db=db,
                event_type=NotificationType.GROUP_ROLE_CHANGED,
                user_id=user_id,
                related_id=group_id,
                custom_message=f"Ahora eres administrador del grupo",
                additional_data={
                    "group_id": group_id,
                    "new_role": "admin"
                }
            )

            return member

        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error making admin: {str(e)}"
            )

    @staticmethod
    async def remove_member(
        db: Session,
        group_id: int,
        current_user_id: int,
        user_id: int
    ) -> None:
        """Remove a member from group"""
        try:
            # Check if current user is owner or admin
            current_member = db.query(GroupMember).filter(
                GroupMember.group_id == group_id,
                GroupMember.user_id == current_user_id
            ).first()

            if not current_member or (not current_member.admin and current_user_id != db.query(Group.owner_id).filter(Group.group_id == group_id).scalar()):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Only owner and admins can remove members"
                )

            # Get target member
            member = db.query(GroupMember).filter(
                GroupMember.group_id == group_id,
                GroupMember.user_id == user_id
            ).first()

            if not member:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User is not a member of this group"
                )

            # Can't remove owner
            if user_id == db.query(Group.owner_id).filter(Group.group_id == group_id).scalar():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Cannot remove group owner"
                )

            db.delete(member)
            db.commit()

            # Notify removed member
            await NotificationService.create_notification_for_event(
                db=db,
                event_type=NotificationType.GROUP_MEMBER_REMOVED,
                user_id=user_id,
                related_id=group_id,
                custom_message=f"Has sido removido del grupo: {Group.name_group}",
                additional_data={
                    "group_id": group_id,
                    "group_name": Group.name_group,
                    "removed_by": current_user_id
                }
            )

        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error removing member: {str(e)}"
            )

    @staticmethod
    async def get_members(
        db: Session,
        group_id: int,
        current_user_id: int,
        skip: int = 0,
        limit: int = 20,
        admin_only: bool = False
    ) -> List[GroupMember]:
        """Get group members"""
        try:
            # Check access to private group
            group = db.query(Group).filter(Group.group_id == group_id).first()
            if not group:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Group not found"
                )

            if group.privacy:
                member = db.query(GroupMember).filter(
                    GroupMember.group_id == group_id,
                    GroupMember.user_id == current_user_id
                ).first()

                if not member and group.owner_id != current_user_id:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Not authorized to view members"
                    )

            query = db.query(GroupMember).filter(GroupMember.group_id == group_id)

            if admin_only:
                query = query.filter(GroupMember.admin == True)

            return query.order_by(GroupMember.joined_at)\
                .offset(skip)\
                .limit(limit)\
                .all()

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error retrieving members: {str(e)}"
            )

    @staticmethod
    async def get_posts(
        db: Session,
        group_id: int,
        current_user_id: int,
        skip: int = 0,
        limit: int = 10
    ) -> List[GroupPost]:
        """Get group posts"""
        try:
            # Check access to private group
            group = db.query(Group).filter(Group.group_id == group_id).first()
            if not group:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Group not found"
                )

            if group.privacy:
                member = db.query(GroupMember).filter(
                    GroupMember.group_id == group_id,
                    GroupMember.user_id == current_user_id
                ).first()

                if not member and group.owner_id != current_user_id:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Not authorized to view posts"
                    )

            return db.query(GroupPost)\
                .filter(GroupPost.group_id == group_id)\
                .order_by(desc(GroupPost.created_at))\
                .offset(skip)\
                .limit(limit)\
                .all()

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error retrieving posts: {str(e)}"
            )

    @staticmethod
    async def delete_post(
        db: Session,
        group_id: int,
        post_id: int,
        current_user_id: int
    ) -> None:
        """Delete a group post"""
        try:
            post = db.query(GroupPost).filter(
                GroupPost.group_id == group_id,
                GroupPost.group_post_id == post_id
            ).first()

            if not post:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Post not found"
                )

            # Check if user is post author, group owner or admin
            is_author = post.user_id == current_user_id
            is_owner = db.query(Group.owner_id).filter(Group.group_id == group_id).scalar() == current_user_id
            is_admin = db.query(GroupMember).filter(
                GroupMember.group_id == group_id,
                GroupMember.user_id == current_user_id,
                GroupMember.admin == True
            ).first() is not None

            if not (is_author or is_owner or is_admin):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not authorized to delete this post"
                )

            db.delete(post)
            db.commit()

        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error deleting post: {str(e)}"
            )

    @staticmethod
    async def upload_group_image(
        db: Session,
        group_id: int,
        current_user_id: int,
        file: UploadFile
    ) -> Group:
        """Upload group image"""
        try:
            group = db.query(Group).filter(Group.group_id == group_id).first()
            if not group:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Group not found"
                )

            # Check if user is owner or admin
            is_owner = group.owner_id == current_user_id
            is_admin = db.query(GroupMember).filter(
                GroupMember.group_id == group_id,
                GroupMember.user_id == current_user_id,
                GroupMember.admin == True
            ).first() is not None

            if not (is_owner or is_admin):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Only owner and admins can update group image"
                )

            # Create directory if it doesn't exist
            media_directory = "uploads/groups"
            os.makedirs(media_directory, exist_ok=True)

            # Validate file extension
            file_extension = os.path.splitext(file.filename)[1].lower()
            if file_extension not in ['.jpg', '.jpeg', '.png']:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid file extension. Only .jpg, .jpeg and .png are allowed"
                )

            # Generate unique filename
            unique_filename = f"group_{group_id}_{uuid.uuid4()}{file_extension}"
            file_location = os.path.join(media_directory, unique_filename)

            # Save file
            try:
                contents = await file.read()
                with open(file_location, "wb") as f:
                    f.write(contents)
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Error saving file: {str(e)}"
                )

            # Delete old image if exists
            if group.group_picture and os.path.exists(group.group_picture):
                try:
                    os.remove(group.group_picture)
                except Exception:
                    pass  # Ignore errors deleting old file

            # Update database
            group.group_picture = file_location
            db.commit()
            db.refresh(group)
            
            return group

        except HTTPException:
            # Si hay una imagen nueva guardada pero ocurrió un error, la eliminamos
            if 'file_location' in locals() and os.path.exists(file_location):
                try:
                    os.remove(file_location)
                except Exception:
                    pass
            raise
        except Exception as e:
            # Si hay una imagen nueva guardada pero ocurrió un error, la eliminamos
            if 'file_location' in locals() and os.path.exists(file_location):
                try:
                    os.remove(file_location)
                except Exception:
                    pass
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error uploading group image: {str(e)}"
            )
    @staticmethod
    async def create_comment(
        db: Session,
        group_id: int,
        post_id: int,
        user_id: int,
        comment_data: GroupCommentCreate
    ) -> GroupComment:
        """Create a comment on a group post"""
        try:
            # Verify membership
            member = db.query(GroupMember).filter(
                GroupMember.group_id == group_id,
                GroupMember.user_id == user_id
            ).first()

            if not member:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Must be a member to comment"
                )

            # Verify post exists and belongs to group
            post = db.query(GroupPost).filter(
                GroupPost.group_post_id == post_id,
                GroupPost.group_id == group_id
            ).first()

            if not post:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Post not found"
                )

            comment = GroupComment(
                group_post_id=post_id,
                user_id=user_id,
                pet_id=member.pet_id,
                comment=comment_data.comment
            )

            db.add(comment)
            
            # Notify post author
            if post.user_id != user_id:
                await NotificationService.create_notification_for_event(
                    db=db,
                    event_type=NotificationType.NEW_COMMENT,
                    user_id=post.user_id,
                    related_id=post_id,
                    custom_message=f"New comment on your post in group"
                )

            db.commit()
            db.refresh(comment)
            return comment

        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating comment: {str(e)}"
            )

    @staticmethod
    async def get_post_comments(
        db: Session,
        group_id: int,
        post_id: int,
        user_id: int,
        skip: int = 0,
        limit: int = 20
    ) -> List[GroupComment]:
        """Get comments for a group post"""
        try:
            # Verify access to group
            group = db.query(Group).filter(Group.group_id == group_id).first()
            if not group:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Group not found"
                )

            if group.privacy:
                member = db.query(GroupMember).filter(
                    GroupMember.group_id == group_id,
                    GroupMember.user_id == user_id
                ).first()

                if not member and group.owner_id != user_id:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Not authorized to view comments"
                    )

            return db.query(GroupComment)\
                .filter(GroupComment.group_post_id == post_id)\
                .order_by(GroupComment.created_at)\
                .offset(skip)\
                .limit(limit)\
                .all()

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error retrieving comments: {str(e)}"
            )

    @staticmethod
    async def delete_comment(
        db: Session,
        group_id: int,
        comment_id: int,
        user_id: int
    ) -> None:
        """Delete a comment"""
        try:
            comment = db.query(GroupComment).join(GroupPost).filter(
                GroupComment.group_comment_id == comment_id,
                GroupPost.group_id == group_id
            ).first()

            if not comment:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Comment not found"
                )

            # Check if user is comment author, group owner or admin
            is_author = comment.user_id == user_id
            is_owner = db.query(Group.owner_id).filter(Group.group_id == group_id).scalar() == user_id
            is_admin = db.query(GroupMember).filter(
                GroupMember.group_id == group_id,
                GroupMember.user_id == user_id,
                GroupMember.admin == True
            ).first() is not None

            if not (is_author or is_owner or is_admin):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not authorized to delete this comment"
                )

            db.delete(comment)
            db.commit()

        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error deleting comment: {str(e)}"
            )

    @staticmethod
    async def transfer_ownership(
        db: Session,
        group_id: int,
        current_user_id: int,
        new_owner_id: int
    ) -> Group:
        """Transfer group ownership to another member"""
        try:
            group = db.query(Group).filter(Group.group_id == group_id).first()
            if not group:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Group not found"
                )

            # Verify current user is owner
            if group.owner_id != current_user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Only the owner can transfer ownership"
                )

            # Verify new owner is a member
            new_owner_member = db.query(GroupMember).filter(
                GroupMember.group_id == group_id,
                GroupMember.user_id == new_owner_id
            ).first()

            if not new_owner_member:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="New owner must be a group member"
                )

            # Update group owner
            group.owner_id = new_owner_id

            # Make new owner admin if not already
            new_owner_member.admin = True

            db.commit()
            db.refresh(group)

            # Notify new owner
            await NotificationService.create_notification_for_event(
                db=db,
                event_type=NotificationType.SYSTEM,
                user_id=new_owner_id,
                related_id=group_id,
                custom_message=f"You are now the owner of the group: {group.name_group}"
            )

            return group

        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error transferring ownership: {str(e)}"
            )

    @staticmethod
    async def attach_media_to_post(
        db: Session,
        group_id: int,
        post_id: int,
        user_id: int,
        files: List[UploadFile]
    ) -> List[MediaFile]:
        """Attach media files to a group post"""
        try:
            # Verify post exists and user has access
            post = db.query(GroupPost).filter(
                GroupPost.group_post_id == post_id,
                GroupPost.group_id == group_id
            ).first()

            if not post:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Post not found"
                )

            if post.user_id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Can only attach media to your own posts"
                )

            media_files = []
            media_directory = "uploads/groups/posts"
            os.makedirs(media_directory, exist_ok=True)

            for file in files:
                # Validate file extension
                file_extension = os.path.splitext(file.filename)[1].lower()
                if file_extension not in ['.jpg', '.jpeg', '.png', '.gif', '.mp4']:
                    continue

                # Generate unique filename
                unique_filename = f"post_{post_id}_{uuid.uuid4()}{file_extension}"
                file_location = os.path.join(media_directory, unique_filename)

                # Save file
                contents = await file.read()
                with open(file_location, "wb") as f:
                    f.write(contents)

                # Create media file record
                media_file = MediaFile(
                    user_id=user_id,
                    group_post_id=post_id,
                    media_url=file_location,
                    media_type="image" if file_extension in ['.jpg', '.jpeg', '.png', '.gif'] else "video"
                )

                db.add(media_file)
                media_files.append(media_file)

            db.commit()
            for media_file in media_files:
                db.refresh(media_file)

            return media_files

        except HTTPException:
            raise
        except Exception as e:
            # Cleanup any saved files on error
            for media_file in media_files:
                if os.path.exists(media_file.media_url):
                    os.remove(media_file.media_url)
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error attaching media: {str(e)}"
            )    