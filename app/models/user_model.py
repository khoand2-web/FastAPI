# app/models/user.py
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from app.db.database import Base


class User(Base):
    """
    User table.

    Note: hashed_password must NEVER be returned to API clients.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(150), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)

    cart = relationship("Cart", back_populates="user", uselist=False,
        cascade="all, delete-orphan",)
