# app/routers/cart_router.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.cart_schema import (
    CartRead,
    CartItemCreate,
    CartItemUpdate
)
from app.services.cart_service import CartService
from app.dependencies.auth_user import get_current_user

router = APIRouter(prefix="/cart", tags=["Cart"])


@router.get("/", response_model=CartRead)
def get_cart(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return CartService.get_or_create_cart(db, current_user.id)


@router.post("/items", status_code=status.HTTP_201_CREATED)
def add_item(
    data: CartItemCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return CartService.add_item(db, current_user.id, data)


@router.put("/items/{item_id}")
def update_item(
    item_id: int,
    data: CartItemUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return CartService.update_item(db, current_user.id, item_id, data)


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def clear_cart(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    CartService.clear_cart(db, current_user.id)
