from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    """Schema for returning access tokens."""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Schema for representing JWT token payload."""
    username: Optional[str] = None


class LoginRequest(BaseModel):
    """Schema for login request body."""
    username: str
    password: str
    
class TokenPayload(BaseModel):
    sub: str | None = None
    exp: int | None = None

