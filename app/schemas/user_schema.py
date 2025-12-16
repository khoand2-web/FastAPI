# app/schemas/user.py
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    """Request schema for creating a user."""
    username: str
    email: EmailStr
    password: str


class UserRead(BaseModel):
    """Response schema for returning a user (safe, no password)."""
    id: int
    username: str
    email: EmailStr
    is_active: bool
    is_superuser: bool

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """Schema for login request if using JSON instead of form."""
    username: str
    password: str
