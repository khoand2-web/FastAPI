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
    product_id: int
    quantity: int

    class Config:
        from_attributes = True


class CartResponse(BaseModel):
    id: int
    user_id: int
    created_at: datetime
    items: List[CartItemResponse]

    class Config:
        from_attributes = True
