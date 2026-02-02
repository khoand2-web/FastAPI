import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from app.db.database import Base, get_db
from app.main import app
from app.models.user_model import User
from app.core.security import hash_password, create_access_token


# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    """Tạo database test mới cho mỗi test."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db: Session):
    """Tạo test client với database test."""
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(db: Session) -> User:
    """Tạo test user."""
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password=hash_password("testpassword123"),  # Dùng hash_password
        is_active=True,
        is_superuser=False,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def test_superuser(db: Session) -> User:
    """Tạo test superuser."""
    user = User(
        username="admin",
        email="admin@example.com",
        hashed_password=hash_password("adminpassword123"),  # Dùng hash_password
        is_active=True,
        is_superuser=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def user_token(test_user: User) -> str:
    """Tạo JWT token cho test user."""
    return create_access_token(subject=str(test_user.id))


@pytest.fixture
def superuser_token(test_superuser: User) -> str:
    """Tạo JWT token cho superuser."""
    return create_access_token(subject=str(test_superuser.id))


@pytest.fixture
def auth_headers(user_token: str) -> dict:
    """Tạo authorization headers với user token."""
    return {"Authorization": f"Bearer {user_token}"}


@pytest.fixture
def superuser_auth_headers(superuser_token: str) -> dict:
    """Tạo authorization headers với superuser token."""
    return {"Authorization": f"Bearer {superuser_token}"}