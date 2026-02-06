# app/services/order_service.py
from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.order_model import Order
from app.models.order_item_model import OrderItem
from app.repositories.product_repository import ProductRepository
from app.schemas.order_schema import OrderCreate


<<<<<<< HEAD
def create_order(db: Session, user_id: int, order_in: OrderCreate) -> Order:
=======

def create_order(db: Session, user_id: int, items: List[dict]) -> Order:
>>>>>>> b55da6f4b54d0f718164ea8ca6a2d658eb20a832
    """
    Create a simple order given items list.

    Args:
        db: DB session.
        user_id: buyer id.
        order_in: OrderCreate schema with items.

    Returns:
        Created Order.
    """
    total = 0.0
    for item in order_in.items:
        product = ProductRepository.get_by_id(db, item.product_id)
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")
        total += product.price * item.quantity

    order = Order(user_id=user_id, total=total)
    db.add(order)
    db.commit()
    db.refresh(order)

    for item in order_in.items:
        product = ProductRepository.get_by_id(db, item.product_id)
        oi = OrderItem(order_id=order.id, product_id=product.id, quantity=item.quantity, price=product.price)
        db.add(oi)
    db.commit()
    db.refresh(order)

    return order
