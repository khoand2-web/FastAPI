# app/repositories/user_repo.py
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.user_model import User

from app.schemas.user_schema import UserCreate, UserRead

class UserRepository:
    """Repository for user DB operations."""

    @staticmethod
    def get_by_id(db: Session, user_id: int) -> Optional[User]:
        """
        Get a user by id.

        Args:
            db: DB session.
            user_id: user id.

        Returns:
            User or None.
        """
        return db.get(User, user_id)

    @staticmethod
    def get_by_username(db: Session, username: str) -> Optional[User]:
        """
        Get a user by username.

        Args:
            db: DB session.
            username: username.

        Returns:
            User or None.
        """
        statement = select(User).where(User.username == username)
        return db.execute(statement).scalar_one_or_none()

    @staticmethod
    def get_by_email(db: Session, email: str) -> Optional[User]:
        """Get user by email."""
        statement = select(User).where(User.email == email)
        return db.execute(statement).scalar_one_or_none()

    @staticmethod
    def create(db: Session, *, user_in: UserCreate, hashed_password: str) -> User:
        """
        Create a user record.

        Args:
            db: DB session.
            user_in: data for new user.
            hashed_password: hashed password.

        Returns:
            Created User.
        """
        user = User(
            username=user_in.username,
            email=user_in.email,
            hashed_password=hashed_password,
            is_active=True,
            is_superuser=False,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
