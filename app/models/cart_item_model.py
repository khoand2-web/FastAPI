# app/models/cart_item.py
from sqlalchemy import Column, Integer, ForeignKey
from app.db.database import Base


class CartItem(Base):
    """Simple cart item for a user."""
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
