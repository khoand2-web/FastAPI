# app/routers/auth_router.py
from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from jose import JWTError

from app.db.database import get_db
from app.schemas.auth import Token, LoginRequest
from app.schemas.user_schema import UserCreate, UserRead
from app.services.user_service import UserService
from app.repositories.user_repository import UserRepository
from app.auth.jwt_manager import create_user_token, read_token
from app.core.exceptions import unauthorized

router = APIRouter(prefix="/auth", tags=["auth"])

user_service = UserService(UserRepository())


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)) -> UserRead:
    """
    Register new user.
    """
    try:
        user = user_service.create_user(db, user_in)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    return UserRead.from_orm(user)


@router.post("/token", response_model=Token)
def login_for_token(login: LoginRequest, db: Session = Depends(get_db)) -> dict:
    """
    Login and return JWT token.
    """
    user = user_service.authenticate(db, login.username, login.password)
    if not user:
        raise unauthorized("Incorrect username or password")

    return create_user_token(user.id)


@router.get("/me", response_model=UserRead)
def read_current_user(authorization: str = Header(None), db: Session = Depends(get_db)) -> UserRead:
    """
    Get current user from JWT token in header.
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise unauthorized("Missing or invalid token")

    token = authorization.split(" ")[1]

    try:
        payload = read_token(token)
    except JWTError:
        raise unauthorized("Could not validate credentials")

    if not payload or not payload.sub:
        raise unauthorized("Invalid token payload")

    user = UserRepository.get_by_id(db, int(payload.sub))
    if not user:
        raise unauthorized("User not found")

    return UserRead.from_orm(user)
