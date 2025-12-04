# app/schemas/product.py
from typing import Optional
from sqlmodel import SQLModel


class ProductBase(SQLModel):
    name: str
    price: float


class ProductCreate(ProductBase):
    """Schema dùng khi tạo sản phẩm"""
    pass


class ProductRead(ProductBase):
    """Schema trả về cho client"""
    id: int
    owner_id: Optional[int] = None

    class Config:
        orm_mode = True
