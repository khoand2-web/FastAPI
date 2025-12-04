from fastapi.security import HTTPBearer
from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from sqlmodel import Session
from core.config import settings
from models.user import User
from database import get_session

oauth2 = HTTPBearer()

def get_current_user(
    token: str = Depends(oauth2),
    session: Session = Depends(get_session)
):
    token = token.credentials

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("id")
        if not user_id:
            raise HTTPException(401, "Invalid token")
    except JWTError:
        raise HTTPException(401, "Invalid token")

    user = session.get(User, user_id)
    if not user:
        raise HTTPException(404, "User not found")

    return user
