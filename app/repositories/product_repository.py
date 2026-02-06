# app/repositories/product_repo.py
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.product_model import Product
from app.schemas.product_schema import ProductCreate



class ProductRepository:
    """Repository for product operations."""

    @staticmethod
    def create(db: Session, product_in: ProductCreate) -> Product:
        """Insert new product."""
        product = Product(
            name=product_in.name,
            description=product_in.description,
            price=product_in.price,
            sku=product_in.sku,
        )
        db.add(product)
        db.commit()
        db.refresh(product)
        return product

    @staticmethod
    def list_all(db: Session) -> List[Product]:
        """Return list of all products."""
        statement = select(Product)
        return db.execute(statement).scalars().all()

    @staticmethod
    def get_by_id(db: Session, product_id: int) -> Optional[Product]:
        """Get product by id."""
        return db.get(Product, product_id)
