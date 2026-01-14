# app/schemas/cart_schema.py
from pydantic import BaseModel
from typing import List
from datetime import datetime


class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = 1


class CartItemUpdate(BaseModel):
    quantity: int


class CartItemRead(BaseModel):
    id: int
    product_id: int
    quantity: int

    class Config:
        from_attributes = True


class CartRead(BaseModel):
    id: int
    user_id: int
    created_at: datetime
    items: List[CartItemRead]

    class Config:
        from_attributes = True
