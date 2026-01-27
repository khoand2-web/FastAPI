from pydantic import BaseModel
from typing import List
from datetime import datetime



class CartItemCreate(BaseModel):
    product_id: int
    quantity: int


class CartItemUpdate(BaseModel):
    quantity: int



class CartItemResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int
    created_at: datetime

    class Config:
        from_attributes = True


class CartResponse(BaseModel):
    items: List[CartItemResponse]

    class Config:
        from_attributes = True
