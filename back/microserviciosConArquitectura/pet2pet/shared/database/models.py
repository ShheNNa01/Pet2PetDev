# shared/database/models.py
from datetime import datetime
from sqlalchemy import JSON, Column, Integer, String, Text, DateTime, Boolean, Date, ForeignKey, func
from sqlalchemy.orm import relationship
from shared.database.base import Base

class Role(Base):
    __tablename__ = "roles"
    role_id = Column(Integer, primary_key=True)
    role_name = Column(String(50), nullable=False, unique=True)
    created_at = Column(DateTime(timezone=True), server_default='CURRENT_TIMESTAMP')
    
    users = relationship("User", back_populates="role")
    user_roles = relationship("UserRole", back_populates="role")

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    user_name = Column(String(100), nullable=False)
    user_last_name = Column(String(100), nullable=False)
    user_city = Column(String(150))
    user_country = Column(String(100))
    user_number = Column(String(20))
    user_email = Column(String(254), nullable=False, unique=True)
    user_bio = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default='CURRENT_TIMESTAMP')
    updated_at = Column(DateTime(timezone=True), server_default='CURRENT_TIMESTAMP', onupdate='CURRENT_TIMESTAMP')
    status = Column(Boolean, default=True)
    password = Column(String(100), nullable=False)
    profile_picture = Column(String(255))
    role_id = Column(Integer, ForeignKey('roles.role_id', ondelete='SET NULL'))

    role = relationship("Role", back_populates="users")
    pets = relationship("Pet", back_populates="owner")
    posts = relationship("Post", back_populates="user")
    comments = relationship("Comment", back_populates="user")
    user_roles = relationship("UserRole", back_populates="user")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")

class UserRole(Base):
    __tablename__ = "user_roles"
    user_role_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'))
    role_id = Column(Integer, ForeignKey('roles.role_id', ondelete='CASCADE'))
    assigned_at = Column(DateTime(timezone=True), server_default='CURRENT_TIMESTAMP')

    user = relationship("User", back_populates="user_roles")
    role = relationship("Role", back_populates="user_roles")

class PetType(Base):
    __tablename__ = "pet_types"
    pet_type_id = Column(Integer, primary_key=True)
    type_name = Column(String(30), nullable=False, unique=True)
    created_at = Column(DateTime(timezone=True), server_default='CURRENT_TIMESTAMP')

    breeds = relationship("Breed", back_populates="pet_type")

class Breed(Base):
    __tablename__ = "breeds"
    breed_id = Column(Integer, primary_key=True)
    breed_name = Column(String(30), nullable=False, unique=True)
    pet_type_id = Column(Integer, ForeignKey('pet_types.pet_type_id', ondelete='CASCADE'))
    created_at = Column(DateTime(timezone=True), server_default='CURRENT_TIMESTAMP')

    pet_type = relationship("PetType", back_populates="breeds")
    pets = relationship("Pet", back_populates="breed")

class Pet(Base):
    __tablename__ = "pets"
    pet_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'))
    name = Column(String(50), nullable=False)
    breed_id = Column(Integer, ForeignKey('breeds.breed_id', ondelete='SET NULL'))
    birthdate = Column(Date)
    gender = Column(String(15))
    bio = Column(String(200))
    pet_picture = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default='CURRENT_TIMESTAMP')
    updated_at = Column(DateTime(timezone=True), server_default='CURRENT_TIMESTAMP', onupdate='CURRENT_TIMESTAMP')
    status = Column(Boolean, default=True)

    owner = relationship("User", back_populates="pets")
    breed = relationship("Breed", back_populates="pets")
    posts = relationship("Post", back_populates="pet")
    comments = relationship("Comment", back_populates="pet")
    sent_messages = relationship("PrivateMessage", foreign_keys="[PrivateMessage.sender_pet_id]", back_populates="sender")
    received_messages = relationship("PrivateMessage", foreign_keys="[PrivateMessage.receiver_pet_id]", back_populates="receiver")

class Post(Base):
    __tablename__ = "posts"
    post_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'))
    pet_id = Column(Integer, ForeignKey('pets.pet_id', ondelete='CASCADE'))
    content = Column(Text)
    location = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default='CURRENT_TIMESTAMP')
    updated_at = Column(DateTime(timezone=True), server_default='CURRENT_TIMESTAMP', onupdate='CURRENT_TIMESTAMP')

    user = relationship("User", back_populates="posts")
    pet = relationship("Pet", back_populates="posts")
    comments = relationship("Comment", back_populates="post")
    reactions = relationship("Reaction", back_populates="post")
    media_files = relationship("MediaFile", back_populates="post")

class Comment(Base):
    __tablename__ = "comments"
    comment_id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.post_id', ondelete='CASCADE'))
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'))
    pet_id = Column(Integer, ForeignKey('pets.pet_id', ondelete='CASCADE'))
    comment = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default='CURRENT_TIMESTAMP')
    updated_at = Column(DateTime(timezone=True), server_default='CURRENT_TIMESTAMP', onupdate='CURRENT_TIMESTAMP')

    post = relationship("Post", back_populates="comments")
    user = relationship("User", back_populates="comments")
    pet = relationship("Pet", back_populates="comments")
    media_files = relationship("MediaFile", back_populates="comment")

class Reaction(Base):
    __tablename__ = "reactions"
    reaction_id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.post_id', ondelete='CASCADE'))
    user_id = Column(Integer, ForeignKey('users.user_id'))
    pet_id = Column(Integer, ForeignKey('pets.pet_id'))
    reaction_type = Column(String(50), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default='CURRENT_TIMESTAMP')
    updated_at = Column(DateTime(timezone=True), server_default='CURRENT_TIMESTAMP', onupdate='CURRENT_TIMESTAMP')

    post = relationship("Post", back_populates="reactions")
    user = relationship("User")
    pet = relationship("Pet")

class PrivateMessage(Base):
    __tablename__ = "private_messages"
    message_id = Column(Integer, primary_key=True)
    sender_pet_id = Column(Integer, ForeignKey('pets.pet_id', ondelete='CASCADE'))
    receiver_pet_id = Column(Integer, ForeignKey('pets.pet_id', ondelete='CASCADE'))
    message = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default='CURRENT_TIMESTAMP')
    read_status = Column(Boolean, default=False)

    sender = relationship("Pet", foreign_keys=[sender_pet_id], back_populates="sent_messages")
    receiver = relationship("Pet", foreign_keys=[receiver_pet_id], back_populates="received_messages")

class Group(Base):
    __tablename__ = "groups"
    group_id = Column(Integer, primary_key=True)
    name_group = Column(String(100), nullable=False)
    description = Column(Text)
    owner_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'))
    created_at = Column(DateTime(timezone=True), server_default='CURRENT_TIMESTAMP')
    group_picture = Column(String(255))
    privacy = Column(Boolean, default=True)

    owner = relationship("User")
    members = relationship("GroupMember", back_populates="group")
    posts = relationship("GroupPost", back_populates="group")

class GroupMember(Base):
    __tablename__ = "group_members"
    member_id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey('groups.group_id', ondelete='CASCADE'))
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'))
    pet_id = Column(Integer, ForeignKey('pets.pet_id', ondelete='CASCADE'))
    joined_at = Column(DateTime(timezone=True), server_default='CURRENT_TIMESTAMP')
    admin = Column(Boolean, default=False)

    group = relationship("Group", back_populates="members")
    user = relationship("User")
    pet = relationship("Pet")

class GroupPost(Base):
    __tablename__ = "group_posts"
    group_post_id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey('groups.group_id', ondelete='CASCADE'))
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'))
    pet_id = Column(Integer, ForeignKey('pets.pet_id', ondelete='CASCADE'))
    content = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default='CURRENT_TIMESTAMP')

    group = relationship("Group", back_populates="posts")
    user = relationship("User")
    pet = relationship("Pet")
    comments = relationship("GroupComment", back_populates="post")
    media_files = relationship("MediaFile", back_populates="group_post")

class GroupComment(Base):
    __tablename__ = "group_comments"
    group_comment_id = Column(Integer, primary_key=True)
    group_post_id = Column(Integer, ForeignKey('group_posts.group_post_id', ondelete='CASCADE'))
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'))
    pet_id = Column(Integer, ForeignKey('pets.pet_id', ondelete='CASCADE'))
    comment = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default='CURRENT_TIMESTAMP')

    post = relationship("GroupPost", back_populates="comments")
    user = relationship("User")
    pet = relationship("Pet")
    media_files = relationship("MediaFile", back_populates="group_comment")

class MediaFile(Base):
    __tablename__ = "media_files"
    media_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    post_id = Column(Integer, ForeignKey('posts.post_id'))
    group_post_id = Column(Integer, ForeignKey('group_posts.group_post_id'))
    comment_id = Column(Integer, ForeignKey('comments.comment_id'))
    group_comment_id = Column(Integer, ForeignKey('group_comments.group_comment_id'))
    media_url = Column(String(255))
    media_type = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default='CURRENT_TIMESTAMP')

    user = relationship("User")
    post = relationship("Post", back_populates="media_files")
    group_post = relationship("GroupPost", back_populates="media_files")
    comment = relationship("Comment", back_populates="media_files")
    group_comment = relationship("GroupComment", back_populates="media_files")

class Report(Base):
    __tablename__ = "reports"
    report_id = Column(Integer, primary_key=True)
    reported_by_user_id = Column(Integer, ForeignKey('users.user_id'))
    reported_content_id = Column(Integer)
    reason = Column(Text)
    status = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default='CURRENT_TIMESTAMP')

    reported_by = relationship("User")

class Follower(Base):
    __tablename__ = "followers"
    follower_id = Column(Integer, primary_key=True)
    follower_pet_id = Column(Integer, ForeignKey('pets.pet_id', ondelete='CASCADE'))
    followed_pet_id = Column(Integer, ForeignKey('pets.pet_id', ondelete='CASCADE'))
    created_at = Column(DateTime(timezone=True), server_default='CURRENT_TIMESTAMP')

    follower = relationship("Pet", foreign_keys=[follower_pet_id])
    followed = relationship("Pet", foreign_keys=[followed_pet_id])

class Friendship(Base):
    __tablename__ = "friendships"
    friendship_id = Column(Integer, primary_key=True)
    pet_id_1 = Column(Integer, ForeignKey('pets.pet_id', ondelete='CASCADE'))
    pet_id_2 = Column(Integer, ForeignKey('pets.pet_id', ondelete='CASCADE'))
    status = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default='CURRENT_TIMESTAMP')

    pet1 = relationship("Pet", foreign_keys=[pet_id_1])
    pet2 = relationship("Pet", foreign_keys=[pet_id_2])

class Notification(Base):
    __tablename__ = "notifications"
    
    notification_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete="CASCADE"))
    type = Column(String(100), nullable=False)
    related_id = Column(Integer, nullable=True)
    message = Column(String(500), nullable=False)  # Añadido para el contenido del mensaje
    is_read = Column(Boolean, default=False)
    additional_data = Column(JSON, nullable=True)  # Añadido para datos extras
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())  # Añadido para tracking de actualizaciones

    # Relaciones
    user = relationship("User", back_populates="notifications")

    def __repr__(self):
        return f"<Notification(id={self.notification_id}, type={self.type}, user_id={self.user_id})>"