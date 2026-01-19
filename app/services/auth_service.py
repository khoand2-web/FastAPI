from datetime import timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.services.user_service import UserService
from app.core.security import create_access_token
from app.core.config import settings


class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def login(self, db: Session, username: str, password: str) -> str:
        user = self.user_service.authenticate(db, username, password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token_expires = timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

        return create_access_token(
            subject=user.id,
            expires_delta=access_token_expires,
        )
