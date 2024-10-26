from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime

from shared.database.models import Group, GroupMember, GroupPost, GroupComment, User, Pet
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
                event_type=NotificationType.NEW_FOLLOWER,  # You might want to create a specific type for this
                user_id=group.owner_id,
                related_id=group_id,
                custom_message=f"New member joined your group: {group.name_group}"
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
            return post

        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating post: {str(e)}"
            )

    # Añadir más métodos según se necesiten...