# app/schemas/product.py
from typing import Optional
from pydantic import BaseModel


class ProductCreate(BaseModel):
    """Schema to create a product."""
    name: str
    description: Optional[str] = None
    price: float
    sku: Optional[str] = None


class ProductRead(BaseModel):
    """Schema to return product info."""
    id: int
    name: str
    description: Optional[str]
    price: float
    sku: Optional[str]

    class Config:
         from_attributes = True
