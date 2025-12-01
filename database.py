from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = "postgresql+psycopg2://postgres:230303@localhost:5432/shopdb"
# nhớ đổi password nếu bạn đặt khác

engine = create_engine(DATABASE_URL, echo=True)


def create_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
