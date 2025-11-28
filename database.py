from sqlmodel import SQLModel, create_engine, Session

from models.user import User
from models.product import Product   # bắt buộc để tạo bảng

DATABASE_URL = "sqlite:///./Shop.db"

engine = create_engine(DATABASE_URL, echo=True)


def create_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
