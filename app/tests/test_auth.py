# app/tests/test_auth.py
"""
Tests cho authentication endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.user_model import User


class TestRegister:
    """Test user registration."""

    def test_register_new_user(self, client: TestClient):
        """Test đăng ký user mới thành công."""
        response = client.post(
            "/auth/register",
            json={
                "username": "newuser",
                "email": "newuser@example.com",
                "password": "password123",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["username"] == "newuser"
        assert data["email"] == "newuser@example.com"
        assert "id" in data
        assert "hashed_password" not in data  # Password không được trả về

    def test_register_duplicate_username(self, client: TestClient, test_user: User):
        """Test đăng ký với username đã tồn tại."""
        response = client.post(
            "/auth/register",
            json={
                "username": test_user.username,
                "email": "different@example.com",
                "password": "password123",
            },
        )
        assert response.status_code == 400

    def test_register_duplicate_email(self, client: TestClient, test_user: User):
        """Test đăng ký với email đã tồn tại."""
        response = client.post(
            "/auth/register",
            json={
                "username": "differentuser",
                "email": test_user.email,
                "password": "password123",
            },
        )
        assert response.status_code == 400

    def test_register_invalid_email(self, client: TestClient):
        """Test đăng ký với email không hợp lệ."""
        response = client.post(
            "/auth/register",
            json={
                "username": "newuser",
                "email": "invalid-email",
                "password": "password123",
            },
        )
        assert response.status_code == 422  # Validation error

    def test_register_weak_password(self, client: TestClient):
        """Test đăng ký với password yếu."""
        response = client.post(
            "/auth/register",
            json={
                "username": "newuser",
                "email": "newuser@example.com",
                "password": "123",  # Too short
            },
        )
        # Tùy vào validation rules của bạn
        assert response.status_code in [400, 422]


class TestLogin:
    """Test user login."""

    def test_login_success(self, client: TestClient, test_user: User):
        """Test login thành công."""
        response = client.post(
            "/auth/login",
            data={
                "username": test_user.username,
                "password": "testpassword123",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_wrong_password(self, client: TestClient, test_user: User):
        """Test login với password sai."""
        response = client.post(
            "/auth/login",
            data={
                "username": test_user.username,
                "password": "wrongpassword",
            },
        )
        assert response.status_code == 401

    def test_login_nonexistent_user(self, client: TestClient):
        """Test login với user không tồn tại."""
        response = client.post(
            "/auth/login",
            data={
                "username": "nonexistent",
                "password": "password123",
            },
        )
        assert response.status_code == 401

    def test_login_inactive_user(self, client: TestClient, db: Session):
        """Test login với user inactive."""
        from app.core.security import hash_password
        
        # Tạo inactive user
        inactive_user = User(
            username="inactiveuser",
            email="inactive@example.com",
            hashed_password=hash_password("password123"),
            is_active=False,
        )
        db.add(inactive_user)
        db.commit()

        response = client.post(
            "/auth/login",
            data={
                "username": "inactiveuser",
                "password": "password123",
            },
        )
        assert response.status_code in [401, 403]


class TestCurrentUser:
    """Test get current user endpoint."""

    def test_get_current_user(
        self, client: TestClient, test_user: User, auth_headers: dict
    ):
        """Test lấy thông tin user hiện tại."""
        response = client.get("/auth/me", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == test_user.username
        assert data["email"] == test_user.email
        assert "hashed_password" not in data

    def test_get_current_user_no_token(self, client: TestClient):
        """Test lấy thông tin user mà không có token."""
        response = client.get("/auth/me")
        assert response.status_code == 401

    def test_get_current_user_invalid_token(self, client: TestClient):
        """Test lấy thông tin user với token không hợp lệ."""
        response = client.get(
            "/auth/me", headers={"Authorization": "Bearer invalid_token"}
        )
        assert response.status_code == 401

    def test_get_current_user_expired_token(self, client: TestClient):
        """Test lấy thông tin user với token hết hạn."""
        # Tạo token đã hết hạn
        expired_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxfQ.invalid"
        response = client.get(
            "/auth/me", headers={"Authorization": f"Bearer {expired_token}"}
        )
        assert response.status_code == 401
