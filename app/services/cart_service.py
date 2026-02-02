# app/services/cart_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.repositories.cart_repository import CartRepository
from app.models.cart_item_model import CartItem
from app.schemas.cart_schema import CartItemCreate, CartItemUpdate


class CartService:

    @staticmethod
    def get_or_create_cart(db: Session, user_id: int):
        cart = CartRepository.get_by_user_id(db, user_id)
        if not cart:
            cart = CartRepository.create(db, user_id)
        return cart

    @staticmethod
    def add_item(db: Session, user_id: int, data: CartItemCreate):
        cart = CartService.get_or_create_cart(db, user_id)

        item = CartRepository.get_item(db, cart.id, data.product_id)
        if item:
            item.quantity += data.quantity
            return CartRepository.update_item(db, item)

        item = CartItem(
            cart_id=cart.id,
            product_id=data.product_id,
            quantity=data.quantity
        )
        return CartRepository.add_item(db, item)

    @staticmethod
    def update_item(db: Session, user_id: int, item_id: int, data: CartItemUpdate):
        cart = CartRepository.get_by_user_id(db, user_id)
        if not cart:
            raise HTTPException(status_code=404, detail="Cart not found")

        item = next((i for i in cart.items if i.id == item_id), None)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")

        if data.quantity <= 0:
            CartRepository.delete_item(db, item)
            return None

        item.quantity = data.quantity
        return CartRepository.update_item(db, item)

    @staticmethod
    def clear_cart(db: Session, user_id: int):
        cart = CartRepository.get_by_user_id(db, user_id)
        if not cart:
            return
        CartRepository.clear_cart(db, cart)

    @staticmethod
    def add_to_cart(db: Session, user_id: int, product_id: int, quantity: int):
        """
        Add product to cart. Router-friendly method.
        
        Args:
            db: Database session
            user_id: User ID
            product_id: Product ID to add
            quantity: Quantity to add
        
        Returns:
            Updated or created cart item
        """
        cart = CartService.get_or_create_cart(db, user_id)

        item = CartRepository.get_item(db, cart.id, product_id)
        if item:
            item.quantity += quantity
            return CartRepository.update_item(db, item)

        item = CartItem(
            cart_id=cart.id,
            product_id=product_id,
            quantity=quantity
        )
        return CartRepository.add_item(db, item)

    @staticmethod
    def remove_from_cart(db: Session, user_id: int, product_id: int):
        """
        Remove product from cart.
        
        Args:
            db: Database session
            user_id: User ID
            product_id: Product ID to remove
        
        Raises:
            HTTPException: If cart or item not found
        """
        cart = CartRepository.get_by_user_id(db, user_id)
        if not cart:
            raise HTTPException(status_code=404, detail="Cart not found")

        item = CartRepository.get_item(db, cart.id, product_id)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found in cart")

        CartRepository.delete_item(db, item)
