# app/routers/users_router.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.user_schema import UserRead
from app.repositories.user_repository import UserRepository

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/{user_id}", response_model=UserRead)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
) -> UserRead:
    """
    Get user by id.
    """
    user = UserRepository.get_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return UserRead.model_validate(user)
