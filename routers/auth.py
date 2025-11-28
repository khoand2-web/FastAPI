from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

from models.user import User
from schemas.user import UserCreate
from database import get_session

router = APIRouter(prefix="/auth", tags=["Auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "your_secret_key_here"
ALGORITHM = "HS256"


def create_access_token(data: dict, expires: int = 60 * 24):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# 🔥 REGISTER
@router.post("/register")
def register(user: UserCreate, session: Session = Depends(get_session)):
    # check email
    exists = session.exec(select(User).where(User.email == user.email)).first()
    if exists:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = pwd_context.hash(user.password)

    new_user = User(
        username=user.username,
        email=user.email,
        password=hashed_pw
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return {"message": "Register successful", "user_id": new_user.id}


# 🔥 LOGIN
@router.post("/login")
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):
    user = session.exec(
        select(User).where(User.username == form.username)
    ).first()

    if not user or not pwd_context.verify(form.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    token = create_access_token({"id": user.id})

    return {"access_token": token, "token_type": "bearer"}
