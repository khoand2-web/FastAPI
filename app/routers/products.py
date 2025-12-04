# app/routers/products.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List

from app.dependencies.session import get_session
from app.schemas.product import ProductCreate, ProductRead
from app.models.product import Product
from app.routers.auth import get_current_user  # đúng vị trí bạn đang dùng

router = APIRouter(prefix="/products", tags=["Products"])


# ---------------- CREATE PRODUCT ----------------
@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(
    data: ProductCreate,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    product = Product(
        name=data.name,
        price=data.price,
        owner_id=current_user.id if current_user else None
    )

    session.add(product)
    session.commit()
    session.refresh(product)
    return product


# ---------------- LIST PRODUCTS ----------------
@router.get("/", response_model=List[ProductRead])
def list_products(session: Session = Depends(get_session)):
    products = session.exec(select(Product)).all()
    return products


# ---------------- GET PRODUCT BY ID ----------------
@router.get("/{product_id}", response_model=ProductRead)
def get_product(product_id: int, session: Session = Depends(get_session)):
    product = session.get(Product, product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


# ---------------- UPDATE PRODUCT ----------------
@router.put("/{product_id}", response_model=ProductRead)
def update_product(
    product_id: int,
    data: ProductCreate,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    product = session.get(Product, product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if product.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed to update this product")

    product.name = data.name
    product.price = data.price

    session.add(product)
    session.commit()
    session.refresh(product)
    return product


# ---------------- DELETE PRODUCT ----------------
@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    product = session.get(Product, product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if product.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed to delete this product")

    session.delete(product)
    session.commit()
    return None
