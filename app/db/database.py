# app/db/database.py
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

from app.core.config import settings

# For SQLite, need check_same_thread
connect_args = {"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(settings.DATABASE_URL, echo=settings.DEBUG, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False, class_=Session)

Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    Provide a transactional scope around a series of operations.

    Yields:
        SQLAlchemy Session for request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
