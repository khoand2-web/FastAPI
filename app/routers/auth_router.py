# app/routers/auth_router.py
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import JWTError

from app.db.database import get_db
from app.schemas.auth import Token, LoginRequest
from app.schemas.user_schema import UserCreate, UserRead
from app.services.user_service import UserService
from app.repositories.user_repository import UserRepository
from app.auth.jwt_manager import create_user_token, read_token
from app.core.exceptions import unauthorized
from app.auth.oauth2 import oauth2_scheme

router = APIRouter(prefix="/auth", tags=["auth"])


def get_user_service() -> UserService:
    return UserService(UserRepository())


@router.post(
    "/register",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
)
def register(
    user_in: UserCreate,
    db: Session = Depends(get_db),
    user_service: UserService = Depends(get_user_service),
) -> UserRead:
    """Register new user."""
    try:
        user = user_service.create_user(db, user_in)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

    return UserRead.model_validate(user)


@router.post("/token", response_model=Token)
def login_for_token(
    login: LoginRequest,
    db: Session = Depends(get_db),
    user_service: UserService = Depends(get_user_service),
) -> Token:
    """Login and return JWT access token."""
    user = user_service.authenticate(db, login.username, login.password)
    if not user:
        raise unauthorized("Incorrect username or password")

    return create_user_token(user.id)


@router.get("/me", response_model=UserRead)
def read_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Session = Depends(get_db),
    user_service: UserService = Depends(get_user_service),
) -> UserRead:
    """Get current authenticated user."""
    try:
        payload = read_token(token)
    except JWTError:
        raise unauthorized("Could not validate credentials")

    if not payload or not payload.sub:
        raise unauthorized("Invalid token payload")

    user = user_service.get_by_id(db, int(payload.sub))
    if not user:
        raise unauthorized("User not found")

    return UserRead.model_validate(user)
