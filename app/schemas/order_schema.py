# app/schemas/order.py
from typing import List
from pydantic import BaseModel


class OrderItemCreate(BaseModel):
    """Request schema for creating an order item."""
    product_id: int
    quantity: int


class OrderCreate(BaseModel):
    """Request schema for creating an order."""
    items: List[OrderItemCreate]


class OrderRead(BaseModel):
    """Response schema for order."""
    id: int
    user_id: int
    total: float

    class Config:
        orm_mode = True
