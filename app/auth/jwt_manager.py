# app/auth/jwt_manager.py
from typing import Optional
from jose import JWTError
from app.core.security import create_access_token, decode_access_token
from app.schemas.auth import TokenPayload


def create_user_token(user_id: int) -> dict:
    """
    Create token payload for user_id.

    Args:
        user_id: numeric id

    Returns:
        dict with access_token and token_type
    """
    token = create_access_token({"sub": str(user_id)})
    return {"access_token": token, "token_type": "bearer"}


def read_token(token: str) -> Optional[TokenPayload]:
    """
    Decode token and return TokenPayload.

    Args:
        token: JWT string

    Returns:
        TokenPayload or raises JWTError
    """
    payload = decode_access_token(token)
    return TokenPayload(**payload)
