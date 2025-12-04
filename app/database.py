from sqlmodel import SQLModel, create_engine
from app.core.config import settings
print("DEBUG ENV:", settings)

engine = create_engine(settings.POSTGRES_URL, echo=True)

def create_db():
    SQLModel.metadata.create_all(engine)
