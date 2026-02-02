# app/routers/product_router.py
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.product_schema import ProductCreate, ProductRead
from app.db.database import get_db
from app.repositories.product_repository import ProductRepository
from app.services.product_service import ProductService


router = APIRouter(prefix="/products", tags=["products"])
product_service = ProductService(ProductRepository())


@router.post("/", response_model=ProductRead)
def create_product(payload: ProductCreate, db: Session = Depends(get_db)) -> ProductRead:
    """
    Create product endpoint.
    """
    product = product_service.create_product(db, payload)
    return ProductRead.from_orm(product)


@router.get("/", response_model=List[ProductRead])
def list_products(db: Session = Depends(get_db)) -> List[ProductRead]:
    """
    List all products.
    """
    items = product_service.list_products(db)
    return [ProductRead.from_orm(i) for i in items]
