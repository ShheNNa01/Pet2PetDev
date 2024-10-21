# post_service.py
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
import jwt

# Configuración de la base de datos
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:123456@localhost:5432/pet2pet"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Configuración de seguridad
SECRET_KEY = "tu_clave_secreta"  # Debe ser la misma que en auth_users_service
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Modelos de la base de datos
class Pet(Base):
    __tablename__ = "pets"
    pet_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))

class Post(Base):
    __tablename__ = "posts"
    post_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    pet_id = Column(Integer, ForeignKey('pets.pet_id'))
    content = Column(Text)
    media_url = Column(String(255))
    location = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    comments = relationship("Comment", back_populates="post")
    reactions = relationship("Reaction", back_populates="post")

class Comment(Base):
    __tablename__ = "comments"
    comment_id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey('posts.post_id'))
    user_id = Column(Integer, ForeignKey('users.user_id'))
    pet_id = Column(Integer, ForeignKey('pets.pet_id'))
    comment = Column(Text)
    media_url = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    post = relationship("Post", back_populates="comments")

class Reaction(Base):
    __tablename__ = "reactions"
    reaction_id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey('posts.post_id'))
    user_id = Column(Integer, ForeignKey('users.user_id'))
    pet_id = Column(Integer, ForeignKey('pets.pet_id'))
    reaction_type = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    post = relationship("Post", back_populates="reactions")

app = FastAPI()

# Modelos Pydantic
class PetBase(BaseModel):
    pet_id: int
    name: str

    class Config:
        orm_mode = True

class PostBase(BaseModel):
    content: str
    media_url: Optional[str] = None
    location: Optional[str] = None
    pet_id: int

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass

class PostInDB(PostBase):
    post_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class CommentBase(BaseModel):
    comment: str
    media_url: Optional[str] = None
    pet_id: int

class CommentCreate(CommentBase):
    pass

class CommentInDB(CommentBase):
    comment_id: int
    post_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class ReactionCreate(BaseModel):
    post_id: int
    pet_id: int
    reaction_type: str

class ReactionInDB(ReactionCreate):
    reaction_id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True

# Funciones de utilidad
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    
    return {"user_id": user_id}

# Endpoint para listar mascotas
@app.get("/pets", response_model=List[PetBase])
async def read_pets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    pets = db.query(Pet).offset(skip).limit(limit).all()
    return pets

# Rutas
@app.post("/posts", response_model=PostInDB)
async def create_post(post: PostCreate, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    pet = db.query(Pet).filter(Pet.pet_id == post.pet_id).first()
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    
    db_post = Post(**post.dict(), user_id=current_user["user_id"])
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

@app.get("/posts", response_model=List[PostInDB])
async def read_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    posts = db.query(Post).offset(skip).limit(limit).all()
    return posts

@app.get("/posts/{post_id}", response_model=PostInDB)
async def read_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.post_id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@app.put("/posts/{post_id}", response_model=PostInDB)
async def update_post(post_id: int, post: PostUpdate, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    db_post = db.query(Post).filter(Post.post_id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    if db_post.user_id != current_user["user_id"]:
        raise HTTPException(status_code=403, detail="Not authorized to update this post")
    for key, value in post.dict().items():
        setattr(db_post, key, value)
    db_post.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_post)
    return db_post

@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    db_post = db.query(Post).filter(Post.post_id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    if db_post.user_id != current_user["user_id"]:
        raise HTTPException(status_code=403, detail="Not authorized to delete this post")
    db.delete(db_post)
    db.commit()
    return {"ok": True}

@app.post("/comments", response_model=CommentInDB)
async def create_comment(comment: CommentCreate, post_id: int, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    db_comment = Comment(**comment.dict(), post_id=post_id, user_id=current_user["user_id"])
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

@app.get("/posts/{post_id}/comments", response_model=List[CommentInDB])
async def read_comments(post_id: int, db: Session = Depends(get_db)):
    comments = db.query(Comment).filter(Comment.post_id == post_id).all()
    return comments

@app.post("/reactions", response_model=ReactionInDB)
async def create_reaction(reaction: ReactionCreate, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    db_reaction = Reaction(**reaction.dict(), user_id=current_user["user_id"])
    db.add(db_reaction)
    db.commit()
    db.refresh(db_reaction)
    return db_reaction

@app.get("/posts/{post_id}/reactions", response_model=List[ReactionInDB])
async def read_reactions(post_id: int, db: Session = Depends(get_db)):
    reactions = db.query(Reaction).filter(Reaction.post_id == post_id).all()
    return reactions

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
