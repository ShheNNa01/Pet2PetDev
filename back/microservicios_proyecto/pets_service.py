# pets_service.py
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import List, Optional
import os
import jwt
from passlib.context import CryptContext
from datetime import date


# Configuración de la base de datos
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:123456@localhost:5432/pet2pet")
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Configuración de seguridad
SECRET_KEY = os.getenv("SECRET_KEY", "tu_clave_secreta")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Modelos de la base de datos
class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, nullable=False)
    user_last_name = Column(String, nullable=False)
    user_city = Column(String)
    user_country = Column(String)
    user_number = Column(String)
    user_email = Column(String, unique=True, index=True, nullable=False)
    user_bio = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    status = Column(Boolean, default=True)
    password = Column(String, nullable=False)
    profile_picture = Column(String)
    is_admin = Column(Boolean, default=False)

class PetType(Base):
    __tablename__ = "pet_types"
    pet_type_id = Column(Integer, primary_key=True, index=True)
    type_name = Column(String(30), unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default='CURRENT_TIMESTAMP')

class Breed(Base):
    __tablename__ = "breeds"
    breed_id = Column(Integer, primary_key=True, index=True)
    breed_name = Column(String(30), unique=True, nullable=False)
    pet_type_id = Column(Integer, ForeignKey('pet_types.pet_type_id'))
    created_at = Column(DateTime(timezone=True), server_default='CURRENT_TIMESTAMP')

class Pet(Base):
    __tablename__ = "pets"
    pet_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    name = Column(String(50), nullable=False)
    species = Column(String(50), nullable=False)
    breed_id = Column(Integer, ForeignKey('breeds.breed_id'))
    birthdate = Column(Date)
    gender = Column(String(15))
    bio = Column(String(200))
    pet_picture = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default='CURRENT_TIMESTAMP')
    updated_at = Column(DateTime(timezone=True), server_default='CURRENT_TIMESTAMP', onupdate='CURRENT_TIMESTAMP')
    status = Column(Boolean, default=True)

# Modelos Pydantic
class UserCreate(BaseModel):
    user_name: str
    user_last_name: str
    user_email: str
    password: str
    user_city: Optional[str] = None
    user_country: Optional[str] = None
    user_number: Optional[str] = None
    user_bio: Optional[str] = None

class UserOut(BaseModel):
    user_id: int
    user_name: str
    user_last_name: str
    user_email: str
    user_city: Optional[str]
    user_country: Optional[str]
    user_number: Optional[str]
    user_bio: Optional[str]
    profile_picture: Optional[str]
    is_admin: bool

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class PetTypeBase(BaseModel):
    type_name: str

class PetTypeCreate(PetTypeBase):
    pass

class PetTypeInDB(PetTypeBase):
    pet_type_id: int
    created_at: datetime

    class Config:
        orm_mode = True

class BreedBase(BaseModel):
    breed_name: str
    pet_type_id: int

class BreedCreate(BreedBase):
    pass

class BreedInDB(BreedBase):
    breed_id: int
    created_at: datetime

    class Config:
        orm_mode = True

class PetBase(BaseModel):
    name: str
    species: str
    breed_id: int
    birthdate: Optional[date]
    gender: Optional[str]
    bio: Optional[str]
    pet_picture: Optional[str]

class PetCreate(PetBase):
    pass

class PetUpdate(PetBase):
    pass

class PetInDB(PetBase):
    pet_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    status: bool

    class Config:
        orm_mode = True

app = FastAPI()

# Funciones de utilidad
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email: str = payload.get("sub")
        if user_email is None:
            raise credentials_exception
        token_data = TokenData(email=user_email)
    except jwt.PyJWTError:
        raise credentials_exception
    user = db.query(User).filter(User.user_email == token_data.email).first()
    if user is None:
        raise credentials_exception
    return user

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Rutas
@app.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.user_email == user.user_email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = pwd_context.hash(user.password)
    new_user = User(**user.dict(exclude={"password"}), password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_email == form_data.username).first()
    if not user or not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.user_email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=UserOut)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@app.put("/users/me", response_model=UserOut)
async def update_user(
    user_update: UserCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    for key, value in user_update.dict(exclude={"password", "user_email"}).items():
        setattr(current_user, key, value)
    if user_update.password:
        current_user.password = pwd_context.hash(user_update.password)
    current_user.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(current_user)
    return current_user

@app.post("/pet-types", response_model=PetTypeInDB)
async def create_pet_type(pet_type: PetTypeCreate, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    db_pet_type = PetType(**pet_type.dict())
    db.add(db_pet_type)
    db.commit()
    db.refresh(db_pet_type)
    return db_pet_type

@app.get("/pet-types", response_model=List[PetTypeInDB])
async def read_pet_types(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    pet_types = db.query(PetType).offset(skip).limit(limit).all()
    return pet_types

@app.post("/breeds", response_model=BreedInDB)
async def create_breed(breed: BreedCreate, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    db_breed = Breed(**breed.dict())
    db.add(db_breed)
    db.commit()
    db.refresh(db_breed)
    return db_breed

@app.get("/breeds", response_model=List[BreedInDB])
async def read_breeds(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    breeds = db.query(Breed).offset(skip).limit(limit).all()
    return breeds

@app.post("/pets", response_model=PetInDB)
async def create_pet(pet: PetCreate, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    db_pet = Pet(**pet.dict(), user_id=current_user.user_id)
    db.add(db_pet)
    db.commit()
    db.refresh(db_pet)
    return db_pet

@app.get("/pets", response_model=List[PetInDB])
async def read_pets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    pets = db.query(Pet).offset(skip).limit(limit).all()
    return pets

@app.get("/pets/{pet_id}", response_model=PetInDB)
async def read_pet(pet_id: int, db: Session = Depends(get_db)):
    pet = db.query(Pet).filter(Pet.pet_id == pet_id).first()
    if pet is None:
        raise HTTPException(status_code=404, detail="Pet not found")
    return pet

@app.put("/pets/{pet_id}", response_model=PetInDB)
async def update_pet(
    pet_id: int, 
    pet: PetUpdate, 
    current_user: dict = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    db_pet = db.query(Pet).filter(Pet.pet_id == pet_id, Pet.user_id == current_user.user_id).first()
    if not db_pet:
        raise HTTPException(status_code=404, detail="Pet not found or not authorized")
    
    for key, value in pet.dict(exclude_unset=True).items():
        setattr(db_pet, key, value)
    
    db_pet.updated_at = datetime.now()
    db.commit()
    db.refresh(db_pet)
    
    return db_pet

@app.delete("/pets/{pet_id}", response_model=PetInDB)
async def delete_pet(pet_id: int, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    db_pet = db.query(Pet).filter(Pet.pet_id == pet_id, Pet.user_id == current_user.user_id).first()
    if not db_pet:
        raise HTTPException(status_code=404, detail="Pet not found or not authorized")
    db.delete(db_pet)
    db.commit()
    return db_pet

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
