from datetime import datetime, timedelta
from typing import Optional

from jose import jwt, JWTError
from passlib.hash import argon2

from app.core.config import settings


# ==========================
#  HASH PASSWORD (ARGON2)
# ==========================
def hash_password(password: str) -> str:
    return argon2.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return argon2.verify(password, hashed_password)


# ==========================
#  JWT TOKEN
# ==========================
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()

    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def decode_access_token(token: str):
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        return payload
    except JWTError:
        return None
