from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.schemas.category_schema import CategoryCreate, CategoryUpdate
from app.repositories.category_repository import CategoryRepository
from app.models.category_model import Category


class CategoryService:
    def __init__(self):
        self.repo = CategoryRepository()

    def get_all(self, db: Session):
        return self.repo.get_all(db)

    def get_by_id(self, db: Session, category_id: UUID):
        category = self.repo.get_by_id(db, category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )
        return category

    def create(self, db: Session, data: CategoryCreate):
        if self.repo.get_by_name(db, data.name):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category name already exists"
            )

        if self.repo.get_by_slug(db, data.slug):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category slug already exists"
            )

        category = Category(**data.model_dump())
        return self.repo.create(db, category)

    def update(self, db: Session, category_id: UUID, data: CategoryUpdate):
        category = self.get_by_id(db, category_id)

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(category, field, value)

        return self.repo.update(db, category)

    def delete(self, db: Session, category_id: UUID):
        category = self.get_by_id(db, category_id)
        self.repo.delete(db, category)
