# app/services/auth_service.py

from jose import JWTError
from sqlalchemy.orm import Session

from app.auth.jwt_manager import create_user_token, read_token
from app.core.exceptions import unauthorized
from app.services.user_service import UserService
from app.schemas.auth import Token


class AuthService:
    """
    Handle authentication business logic.

    Responsibilities:
    - Authenticate user credentials
    - Issue JWT access token
    - Resolve current user from JWT token
    """

    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def login(self, db: Session, username: str, password: str) -> Token:
        """
        Authenticate user and return JWT access token.
        """
        user = self.user_service.authenticate(db, username, password)
        if not user:
            raise unauthorized("Incorrect username or password")

        return create_user_token(user.id)

    def get_current_user(self, db: Session, token: str):
        """
        Get current authenticated user from JWT token.
        """
        try:
            payload = read_token(token)
        except JWTError:
            raise unauthorized("Could not validate credentials")

        if not payload or not payload.sub:
            raise unauthorized("Invalid token payload")

        user = self.user_service.get_by_id(db, int(payload.sub))
        if not user:
            raise unauthorized("User not found")

        return user
