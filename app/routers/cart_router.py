from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.cart_schema import CartItemCreate, CartResponse
from app.services.cart_service import CartService
from app.core.security import get_current_user

router = APIRouter(prefix="/cart", tags=["cart"])

cart_service = CartService()


@router.get("/", response_model=CartResponse)
def get_my_cart(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return cart_service.get_or_create_cart(db, current_user.id)


@router.post("/items")
def add_item_to_cart(
    data: CartItemCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return cart_service.add_to_cart(
        db,
        current_user.id,
        data.product_id,
        data.quantity,
    )


@router.delete("/items/{product_id}")
def remove_item_from_cart(
    product_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    cart_service.remove_from_cart(db, current_user.id, product_id)
    return {"message": "Item removed"}
