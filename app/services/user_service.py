# app/services/user_service.py
from typing import Optional

from sqlalchemy.orm import Session

from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserCreate
from app.core.security import hash_password
from app.models.user_model import User


class UserService:
    """Business logic for user operations."""

    def __init__(self, repo: UserRepository):
        """
        Initialize service.

        Args:
            repo: Instance of UserRepository.
        """
        self.repo = repo

    def create_user(self, db: Session, user_in: UserCreate) -> User:
        """
        Create a user after validating uniqueness.

        Args:
            db: DB session
            user_in: user create payload

        Returns:
            Created User
        """
        if self.repo.get_by_username(db, user_in.username):
            raise ValueError("username exists")
        if self.repo.get_by_email(db, user_in.email):
            raise ValueError("email exists")
        hashed = hash_password(user_in.password)
        return self.repo.create(db, user_in=user_in, hashed_password=hashed)

    def authenticate(self, db: Session, username: str, password: str) -> Optional[User]:
        """
        Authenticate a user and return the user object.

        Args:
            db: DB session
            username: username
            password: plaintext password

        Returns:
            User if authenticated else None
        """
        user = self.repo.get_by_username(db, username)
        if not user:
            return None
        from app.core.security import verify_password

        if not verify_password(password, user.hashed_password):
            return None
        return user
