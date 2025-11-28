from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from database import get_session
from models.user import User
from core.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/users", tags=["Users"])

# -------------------------------------------
# ĐĂNG KÝ
# -------------------------------------------
@router.post("/register", response_model=User)
def register(user: User, session: Session = Depends(get_session)):

    # check email tồn tại
    existing = session.exec(select(User).where(User.email == user.email)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user.password = hash_password(user.password)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

# -------------------------------------------
# ĐĂNG NHẬP
# -------------------------------------------
@router.post("/login")
def login(email: str, password: str, session: Session = Depends(get_session)):
    
    user = session.exec(select(User).where(User.email == email)).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    if not verify_password(password, user.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    token = create_access_token({"sub": str(user.id)})

    return {"access_token": token, "token_type": "bearer"}

# -------------------------------------------
# LẤY THÔNG TIN USER TỪ TOKEN
# -------------------------------------------
import jwt
from core.security import SECRET_KEY, ALGORITHM

def get_current_user(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        return user_id
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.get("/profile")
def profile(token: str, session: Session = Depends(get_session)):
    user_id = get_current_user(token)
    user = session.get(User, user_id)
    return user
