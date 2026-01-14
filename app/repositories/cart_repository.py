# app/repositories/cart_repository.py
from sqlalchemy.orm import Session

from app.models.cart_model import Cart
from app.models.cart_item_model import CartItem


class CartRepository:

    @staticmethod
    def get_by_user_id(db: Session, user_id: int) -> Cart | None:
        return db.query(Cart).filter(Cart.user_id == user_id).first()

    @staticmethod
    def create(db: Session, user_id: int) -> Cart:
        cart = Cart(user_id=user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
        return cart

    @staticmethod
    def get_item(db: Session, cart_id: int, product_id: int) -> CartItem | None:
        return (
            db.query(CartItem)
            .filter(
                CartItem.cart_id == cart_id,
                CartItem.product_id == product_id
            )
            .first()
        )

    @staticmethod
    def add_item(db: Session, item: CartItem):
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def delete_item(db: Session, item: CartItem):
        db.delete(item)
        db.commit()

    @staticmethod
    def clear_cart(db: Session, cart: Cart):
        cart.items.clear()
        db.commit()
