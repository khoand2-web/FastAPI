# app/schemas/user.py

from pydantic import BaseModel

# Schema để tạo user
class UserCreate(BaseModel):
    username: str
    password: str


# Schema để trả về thông tin user (không có password)
class UserRead(BaseModel):
    id: int
    username: str

    model_config = {
        "from_attributes": True  # thay thế orm_mode ở Pydantic v2
    }
