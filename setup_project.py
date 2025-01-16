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
    ]

    # Create directories
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

    # Create __init__.py files for packages
    create_file("app/__init__.py")
    create_file("app/routers/__init__.py")
    create_file("app/models/__init__.py")
    create_file("app/schemas/__init__.py")

    # Create main.py
    create_file(
        "app/main.py",
        """from fastapi import FastAPI
from app.routers import example

app = FastAPI()

# Include routers
app.include_router(example.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!"}
""",
    )

    # Create database.py
    create_file(
        "app/database.py",
        """from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import DeclarativeBase
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = DeclarativeBase()
""",
    )

    # Create example router
    create_file(
        "app/routers/example.py",
        """from fastapi import APIRouter

router = APIRouter(
    prefix="/example",
    tags=["Example"],
)

@router.get("/")
def get_example():
    return {"message": "This is an example endpoint"}
""",
    )

    # Create example model
    create_file(
        "app/models/example.py",
        """from sqlalchemy import Column, Integer, String
from app.database import Base

class Example(Base):
    __tablename__ = "examples"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
""",
    )

    # Create example schema
    create_file(
        "app/schemas/example.py",
        """from pydantic import BaseModel

class ExampleSchema(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        orm_mode = True
""",
    )

    # Create requirements.txt
    create_file(
        "requirements.txt",
        """fastapi
uvicorn
sqlalchemy
pydantic
python-dotenv
""",
    )

    # Create .env file
    create_file(
        ".env",
        """DATABASE_URL=sqlite:///./test.db
""",
    )

    print("FastAPI project structure has been set up in the current directory!")


if __name__ == "__main__":
    setup_fastapi_project()
