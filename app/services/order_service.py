# app/services/order_service.py
from typing import List
from sqlalchemy.orm import Session

from app.models.order_model import Order
from app.models.order_item_model import OrderItem
from app.repositories.product_repository import ProductRepository



def create_order(db: Session, user_id: int, items: List[dict]) -> Order:
    """
    Create a simple order given items list [{"product_id": int, "quantity": int}, ...].

    Args:
        db: DB session.
        user_id: buyer id.
        items: list of items.

    Returns:
        Created Order.
    """
    total = 0.0
    for it in items:
        product = ProductRepository.get_by_id(db, it["product_id"])
        if not product:
            raise ValueError(f"Product {it['product_id']} not found")
        total += product.price * it["quantity"]

    order = Order(user_id=user_id, total=total)
    db.add(order)
    db.commit()
    db.refresh(order)

    for it in items:
        product = ProductRepository.get_by_id(db, it["product_id"])
        oi = OrderItem(order_id=order.id, product_id=product.id, quantity=it["quantity"], price=product.price)
        db.add(oi)
    db.commit()

    return order
