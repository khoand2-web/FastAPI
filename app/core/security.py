from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings
from app.db.database import get_db
from app.repositories.user_repository import UserRepository


# ======================================================
# Password hashing (ARGON2 – KHÔNG DÙNG BCRYPT)
# ======================================================

pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto",
)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# ======================================================
# OAuth2
# ======================================================

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# ======================================================
# JWT
# ======================================================

def create_access_token(
    subject: str | int,
    expires_delta: Optional[timedelta] = None,
) -> str:
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )


    to_encode = {
        "exp": expire,
        "sub": str(subject),
    }

    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


def decode_access_token(token: str) -> str:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        subject: str | None = payload.get("sub")
        if subject is None:
            raise JWTError()
        return subject
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )


# ======================================================
# Dependency: get_current_user
# ======================================================

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db=Depends(get_db),
):
    user_id = decode_access_token(token)

    user = UserRepository.get_by_id(db, int(user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user
