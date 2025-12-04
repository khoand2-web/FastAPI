from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List

from app.dependencies.session import get_session
from app.schemas.user import UserCreate, UserRead
from app.models.user import User
from app.security import hash_password, get_current_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserRead)
def create_user(data: UserCreate, session: Session = Depends(get_session)):
    user = User(
        username=data.username,
        email=data.email,
        hashed_password=hash_password(data.password),
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.get("/", response_model=List[UserRead])
def list_users(
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    users = session.exec(select(User)).all()
    return users
