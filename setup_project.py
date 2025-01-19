import os


def create_file(filepath, content=""):
    """Create a file with optional content."""
    with open(filepath, "w") as f:
        f.write(content)


def setup_fastapi_project():
    """Set up the FastAPI project structure in the current directory."""

    # Directory structure
    directories = [
        "app",
        "app/routers",
        "app/models",
        "app/schemas",
        "app/utils",
    ]

    # Create directories
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

    # Create __init__.py files for packages
    for package in ["app", "app/routers", "app/models", "app/schemas", "app/utils"]:
        create_file(f"{package}/__init__.py")

    # main.py
    create_file(
        "app/main.py",
        """from fastapi import FastAPI
from app.routers import users

app = FastAPI()

# Include routers
app.include_router(users.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Authentication API!"}
""",
    )

    # database.py
    create_file(
        "app/database.py",
        """from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import DeclarativeBase
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = DeclarativeBase()

# Dependency for database sessions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
""",
    )

    # utils/auth.py
    create_file(
        "app/utils/auth.py",
        """from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
import os

SECRET_KEY = os.getenv("SECRET_KEY", "default-secret-key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
""",
    )

    # models/user.py
    create_file(
        "app/models/user.py",
        """from sqlalchemy import Column, Integer, String
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
""",
    )

    # schemas/user.py
    create_file(
        "app/schemas/user.py",
        """from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str
""",
    )

    # routers/users.py
    create_file(
        "app/routers/users.py",
        """from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas
from app.utils.auth import get_password_hash, verify_password, create_access_token
from app.database import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

@router.post("/register", response_model=schemas.user.UserOut)
def register_user(user: schemas.user.UserCreate, db: Session = Depends(get_db)):
    if db.query(models.user.User).filter(models.user.User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    if db.query(models.user.User).filter(models.user.User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already taken")

    hashed_password = get_password_hash(user.password)
    new_user = models.user.User(
        username=user.username, email=user.email, hashed_password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post("/login", response_model=schemas.user.Token)
def login_user(user: schemas.user.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.user.User).filter(models.user.User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token(data={"sub": db_user.email})
    return {"access_token": token, "token_type": "bearer"}
""",
    )

    # requirements.txt
    create_file(
        "requirements.txt",
        """fastapi
uvicorn
sqlalchemy
psycopg2-binary
python-jose
passlib
python-dotenv
""",
    )

    # .env
    create_file(
        ".env",
        """DATABASE_URL=postgresql://username:password@localhost:5432/auth_app
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
""",
    )

    print("FastAPI authentication system has been set up in the current directory!")


if __name__ == "__main__":
    setup_fastapi_project()
