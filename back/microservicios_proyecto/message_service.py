# message_service.py
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from pydantic import BaseModel
from datetime import datetime
from typing import List
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

# Modelo de la base de datos para mensajes
class Message(Base):
    __tablename__ = "private_messages"
    message_id = Column(Integer, primary_key=True, index=True)
    sender_pet_id = Column(Integer, ForeignKey('pets.pet_id'))
    receiver_pet_id = Column(Integer, ForeignKey('pets.pet_id'))
    message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    read_status = Column(Boolean, default=False)

# Modelo de la base de datos para mascotas
class Pet(Base):
    __tablename__ = "pets"
    pet_id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey('users.user_id'))  # Cambia 'users.user_id' según tu esquema
    name = Column(String)

    owner = relationship("User")  # Relación con el modelo de usuario

# Aplicación FastAPI
app = FastAPI()

# Modelos Pydantic
class MessageBase(BaseModel):
    message: str

class MessageCreate(MessageBase):
    receiver_pet_id: int

class MessageUpdate(BaseModel):
    read_status: bool

class MessageInDB(MessageBase):
    message_id: int
    sender_pet_id: int
    receiver_pet_id: int
    created_at: datetime
    read_status: bool

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

# Función auxiliar para obtener el pet_id asociado a un usuario
def get_pet_id_for_user(db: Session, user_id: int) -> int:
    pet = db.query(Pet).filter(Pet.owner_id == user_id).first()
    return pet.pet_id if pet else None

# Rutas
@app.post("/messages", response_model=MessageInDB)
async def send_message(message: MessageCreate, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    sender_pet_id = get_pet_id_for_user(db, current_user["user_id"])
    if sender_pet_id is None:
        raise HTTPException(status_code=404, detail="Sender pet not found")
    
    db_message = Message(sender_pet_id=sender_pet_id, **message.dict())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

@app.get("/messages", response_model=List[MessageInDB])
async def read_messages(current_user: dict = Depends(get_current_user), skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    user_pet_id = get_pet_id_for_user(db, current_user["user_id"])
    messages = db.query(Message).filter(
        (Message.sender_pet_id == user_pet_id) | (Message.receiver_pet_id == user_pet_id)
    ).order_by(Message.created_at.desc()).offset(skip).limit(limit).all()
    return messages

@app.get("/messages/{message_id}", response_model=MessageInDB)
async def read_message(message_id: int, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    user_pet_id = get_pet_id_for_user(db, current_user["user_id"])
    message = db.query(Message).filter(
        Message.message_id == message_id,
        ((Message.sender_pet_id == user_pet_id) | (Message.receiver_pet_id == user_pet_id))
    ).first()
    if message is None:
        raise HTTPException(status_code=404, detail="Message not found")
    return message

@app.put("/messages/{message_id}", response_model=MessageInDB)
async def update_message(message_id: int, message_update: MessageUpdate, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    user_pet_id = get_pet_id_for_user(db, current_user["user_id"])
    db_message = db.query(Message).filter(
        Message.message_id == message_id,
        Message.receiver_pet_id == user_pet_id
    ).first()
    if db_message is None:
        raise HTTPException(status_code=404, detail="Message not found")
    db_message.read_status = message_update.read_status
    db.commit()
    db.refresh(db_message)
    return db_message

@app.delete("/messages/{message_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_message(message_id: int, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    user_pet_id = get_pet_id_for_user(db, current_user["user_id"])
    db_message = db.query(Message).filter(
        Message.message_id == message_id,
        ((Message.sender_pet_id == user_pet_id) | (Message.receiver_pet_id == user_pet_id))
    ).first()
    if db_message is None:
        raise HTTPException(status_code=404, detail="Message not found")
    db.delete(db_message)
    db.commit()
    return {"ok": True}

@app.get("/conversations", response_model=List[dict])
async def get_conversations(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    user_pet_id = get_pet_id_for_user(db, current_user["user_id"])
    subquery = db.query(
        Message.sender_pet_id,
        Message.receiver_pet_id,
        Message.created_at.label('last_message_time'),
        Message.message.label('last_message_content')
    ).filter(
        (Message.sender_pet_id == user_pet_id) | (Message.receiver_pet_id == user_pet_id)
    ).order_by(Message.created_at.desc()).subquery()

    conversations = db.query(
        subquery.c.sender_pet_id,
        subquery.c.receiver_pet_id,
        subquery.c.last_message_time,
        subquery.c.last_message_content
    ).distinct(
        (subquery.c.sender_pet_id + subquery.c.receiver_pet_id)
    ).order_by(
        (subquery.c.sender_pet_id + subquery.c.receiver_pet_id),
        subquery.c.last_message_time.desc()
    ).all()

    return [
        {
            "pet_id": conv.sender_pet_id if conv.receiver_pet_id == user_pet_id else conv.receiver_pet_id,
            "last_message_time": conv.last_message_time,
            "last_message_content": conv.last_message_content
        }
        for conv in conversations
    ]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)
