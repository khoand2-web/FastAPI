# app/db/init_db.py
from app.db.database import Base, engine


def init_db() -> None:
    """
    Create DB tables based on models metadata.

    This runs SQLModel/SQLAlchemy Base.metadata.create_all.
    """
    Base.metadata.create_all(bind=engine)
