from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select, Session
from typing import List

from database import get_session
from models.product import Product
from dependencies.auth_user import get_current_user   # ✔ đúng

router = APIRouter(prefix="/products", tags=["Products"])


# CREATE (yêu cầu đăng nhập)
@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
def create_product(
    product: Product,
    session: Session = Depends(get_session),
    user=Depends(get_current_user)    # ✔ yêu cầu JWT
):
    session.add(product)
    session.commit()
    session.refresh(product)
    return product


# LIST
@router.get("/", response_model=List[Product])
def list_products(
    page: int = 1,
    limit: int = 10,
    search: str = None,
    sort: str = None,
    session: Session = Depends(get_session)
):
    query = select(Product)

    if search:
        query = query.where(Product.name.contains(search))

    if sort:
        if sort == "price_asc":
            query = query.order_by(Product.price.asc())
        elif sort == "price_desc":
            query = query.order_by(Product.price.desc())
        elif sort == "name_asc":
            query = query.order_by(Product.name.asc())
        elif sort == "name_desc":
            query = query.order_by(Product.name.desc())

    offset = (page - 1) * limit
    products = session.exec(query.offset(offset).limit(limit)).all()
    return products


# GET ONE
@router.get("/{product_id}", response_model=Product)
def get_product(product_id: int, session: Session = Depends(get_session)):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


# UPDATE (yêu cầu đăng nhập)
@router.put("/{product_id}", response_model=Product)
def update_product(
    product_id: int,
    updated: Product,
    session: Session = Depends(get_session),
    user=Depends(get_current_user)    # ✔ yêu cầu JWT
):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product.name = updated.name
    product.description = updated.description
    product.price = updated.price
    product.in_stock = updated.in_stock

    session.add(product)
    session.commit()
    session.refresh(product)
    return product


# DELETE (yêu cầu đăng nhập)
@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    session: Session = Depends(get_session),
    user=Depends(get_current_user)     # ✔ yêu cầu JWT
):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    session.delete(product)
    session.commit()
    return
