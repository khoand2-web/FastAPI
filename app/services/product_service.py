# app/services/product_service.py
from typing import List, Optional
from sqlalchemy.orm import Session

from app.repositories.product_repository import ProductRepository
from app.schemas.product_schema import ProductCreate
from app.models.product_model import Product


class ProductService:
    """Business logic for products."""

    def __init__(self, repo: ProductRepository):
        self.repo = repo

    def create_product(self, db: Session, payload: ProductCreate) -> Product:
        """
        Create a product in DB.

        Args:
            db: DB session
            payload: product create schema

        Returns:
            Product instance
        """
        return self.repo.create(db, payload)

    def list_products(self, db: Session) -> List[Product]:
        """Return list of products."""
        return self.repo.list_all(db)

    def get_product(self, db: Session, product_id: int) -> Optional[Product]:
        """Return product by id."""
        return self.repo.get_by_id(db, product_id)
