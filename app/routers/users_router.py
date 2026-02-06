# app/routers/user_router.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService
from app.schemas.user_schema import UserCreate, UserRead

router = APIRouter(prefix="/users", tags=["users"])
user_service = UserService(UserRepository())


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate, db: Session = Depends(get_db)) -> UserRead:
    """
    Create a new user.
    """
    try:
        user = user_service.create_user(db, payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    return UserRead.from_orm(user)
