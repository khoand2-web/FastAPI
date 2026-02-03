from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.db.database import get_db
from app.schemas.category_schema import (
    CategoryCreate,
    CategoryUpdate,
    CategoryResponse
)
from app.services.category_service import CategoryService

router = APIRouter(prefix="/categories", tags=["Categories"])
service = CategoryService()


@router.get("/", response_model=List[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    return service.get_all(db)


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: UUID, db: Session = Depends(get_db)):
    return service.get_by_id(db, category_id)


@router.post("/", response_model=CategoryResponse, status_code=201)
def create_category(data: CategoryCreate, db: Session = Depends(get_db)):
    return service.create(db, data)


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: UUID,
    data: CategoryUpdate,
    db: Session = Depends(get_db)
):
    return service.update(db, category_id, data)


@router.delete("/{category_id}", status_code=204)
def delete_category(category_id: UUID, db: Session = Depends(get_db)):
    service.delete(db, category_id)
