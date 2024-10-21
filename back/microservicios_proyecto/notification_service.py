# notification_service.py
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
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

# Modelo de la base de datos
class Notification(Base):
    __tablename__ = "notifications"
    notification_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    type = Column(String(50), nullable=False)
    related_id = Column(Integer)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

app = FastAPI()

# Modelos Pydantic
class NotificationBase(BaseModel):
    type: str
    related_id: Optional[int]

class NotificationCreate(NotificationBase):
    user_id: int

class NotificationUpdate(BaseModel):
    is_read: bool

class NotificationInDB(NotificationBase):
    notification_id: int
    user_id: int
    is_read: bool
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

# Rutas
@app.post("/notifications", response_model=NotificationInDB)
async def create_notification(notification: NotificationCreate, db: Session = Depends(get_db)):
    db_notification = Notification(**notification.dict())
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification

@app.get("/notifications", response_model=List[NotificationInDB])
async def read_notifications(current_user: dict = Depends(get_current_user), skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    notifications = db.query(Notification).filter(Notification.user_id == current_user["user_id"]).offset(skip).limit(limit).all()
    return notifications

@app.get("/notifications/{notification_id}", response_model=NotificationInDB)
async def read_notification(notification_id: int, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    notification = db.query(Notification).filter(Notification.notification_id == notification_id, Notification.user_id == current_user["user_id"]).first()
    if notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notification

@app.put("/notifications/{notification_id}", response_model=NotificationInDB)
async def update_notification(notification_id: int, notification_update: NotificationUpdate, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    db_notification = db.query(Notification).filter(Notification.notification_id == notification_id, Notification.user_id == current_user["user_id"]).first()
    if db_notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    db_notification.is_read = notification_update.is_read
    db.commit()
    db.refresh(db_notification)
    return db_notification

@app.delete("/notifications/{notification_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_notification(notification_id: int, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    db_notification = db.query(Notification).filter(Notification.notification_id == notification_id, Notification.user_id == current_user["user_id"]).first()
    if db_notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    db.delete(db_notification)
    db.commit()
    return {"ok": True}

# Funciones de utilidad para crear notificaciones específicas
def create_follow_notification(db: Session, follower_id: int, followed_id: int):
    notification = NotificationCreate(
        user_id=followed_id,
        type="follow",
        related_id=follower_id
    )
    return create_notification(notification, db)

def create_like_notification(db: Session, liker_id: int, post_owner_id: int, post_id: int):
    notification = NotificationCreate(
        user_id=post_owner_id,
        type="like",
        related_id=post_id
    )
    return create_notification(notification, db)

def create_comment_notification(db: Session, commenter_id: int, post_owner_id: int, post_id: int):
    notification = NotificationCreate(
        user_id=post_owner_id,
        type="comment",
        related_id=post_id
    )
    return create_notification(notification, db)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
