# app/services/user_service.py
from typing import Optional

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserCreate
from app.core.security import hash_password, verify_password
from app.models.user_model import User


class UserService:
    """Business logic for user operations."""

    def __init__(self, repo: UserRepository):
        self.repo = repo

    def create_user(self, db: Session, user_in: UserCreate) -> User:
        """
        Create a user after validating uniqueness.
        """
        if self.repo.get_by_username(db, user_in.username):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username already exists",
            )

        if self.repo.get_by_email(db, user_in.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already exists",
            )

        hashed_password = hash_password(user_in.password)
        return self.repo.create(
            db,
            user_in=user_in,
            hashed_password=hashed_password,
        )

    def authenticate(
        self,
        db: Session,
        username: str,
        password: str,
    ) -> Optional[User]:
        """
        Authenticate a user and return the user object.
        """
        user = self.repo.get_by_username(db, username)
        if not user:
            return None

        if not verify_password(password, user.hashed_password):
            return None

        return user
