import uuid
from sqlalchemy import Column, String, Boolean, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    slug = Column(String(255), nullable=False)
    description = Column(String(500), nullable=True)

    parent_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"), nullable=True)

    is_active = Column(Boolean, default=True, nullable=False)

    parent = relationship(
        "Category",
        remote_side=[id],
        backref="children"
    )

    __table_args__ = (
        Index("ix_categories_name_unique", "name", unique=True),
        Index("ix_categories_slug_unique", "slug", unique=True),
    )
