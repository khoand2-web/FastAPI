from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List

from database import get_session
from models.user import User
from dependencies.auth_user import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])


# ---------------------------------------------------
# GET CURRENT USER (based on token)
# ---------------------------------------------------
@router.get("/me", response_model=User)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


# ---------------------------------------------------
# GET ONE USER (admin only)
# ---------------------------------------------------
@router.get("/{user_id}", response_model=User)
def get_user(user_id: int, 
             session: Session = Depends(get_session),
             current_user: User = Depends(get_current_user)):
    
    # Allow only admin view (simple rule: id == 1)
    if current_user.id != 1:
        raise HTTPException(status_code=403, detail="Admin only")

    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


# ---------------------------------------------------
# LIST ALL USERS (admin only)
# ---------------------------------------------------
@router.get("/", response_model=List[User])
def list_users(session: Session = Depends(get_session),
               current_user: User = Depends(get_current_user)):
    
    if current_user.id != 1:
        raise HTTPException(status_code=403, detail="Admin only")

    users = session.exec(select(User)).all()
    return users
