from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas
from app.utils.auth import get_password_hash, verify_password, create_access_token, get_current_user
from app.database import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

# Register a new user
@router.post("/register", response_model=schemas.user.UserOut, summary="Register a new user")
def register_user(user: schemas.user.UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user with a unique email and username.
    """
    if db.query(models.user.User).filter(models.user.User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    if db.query(models.user.User).filter(models.user.User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already taken")

    hashed_password = get_password_hash(user.password)
    new_user = models.user.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# Log in and get a JWT token
@router.post("/login", response_model=schemas.user.Token, summary="Log in and get a JWT token")
def login_user(user: schemas.user.UserCreate, db: Session = Depends(get_db)):
    """
    Authenticate the user and return a JWT token.
    """
    db_user = db.query(models.user.User).filter(models.user.User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token(data={"sub": db_user.email})
    return {"access_token": token, "token_type": "bearer"}


# Get the current user's profile
@router.get("/me", response_model=schemas.user.UserOut, summary="Get current user's profile")
def get_user_profile(current_user: models.user.User = Depends(get_current_user)):
    """
    Fetch the profile of the currently authenticated user.
    Requires Bearer Token Authorization.
    """
    return current_user
