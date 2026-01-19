# app/routers/auth_router.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.auth import LoginRequest, Token
from app.schemas.user_schema import UserCreate, UserRead
from app.services.user_service import UserService
from app.services.auth_service import AuthService
from app.repositories.user_repository import UserRepository
from app.core.security import get_current_user
from app.models.user_model import User

router = APIRouter(prefix="/auth", tags=["Auth"])


def get_user_service():
    return UserService(UserRepository())


def get_auth_service(
    user_service: UserService = Depends(get_user_service),
):
    return AuthService(user_service)


@router.post(
    "/register",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
)
def register(
    user_in: UserCreate,
    db: Session = Depends(get_db),
    user_service: UserService = Depends(get_user_service),
):
    user = user_service.create_user(db, user_in)
    return UserRead.model_validate(user)


@router.post("/token", response_model=Token)
def login_for_token(
    login: LoginRequest,
    db: Session = Depends(get_db),
    auth_service: AuthService = Depends(get_auth_service),
):
    access_token = auth_service.login(db, login.username, login.password)
    return Token(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=UserRead)
def read_current_user(
    current_user: User = Depends(get_current_user),
):
    return UserRead.model_validate(current_user)
