# app/tests/test_users.py
"""
Tests cho user management endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.user_model import User


class TestCreateUser:
    """Test user creation endpoint."""

    def test_create_user_success(self, client: TestClient):
        """Test tạo user mới thành công."""
        response = client.post(
            "/users/",
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

    def test_create_user_duplicate_username(self, client: TestClient, test_user: User):
        """Test tạo user với username đã tồn tại."""
        response = client.post(
            "/users/",
            json={
                "username": test_user.username,
                "email": "different@example.com",
                "password": "password123",
            },
        )
        assert response.status_code == 400

    def test_create_user_invalid_data(self, client: TestClient):
        """Test tạo user với dữ liệu không hợp lệ."""
        response = client.post(
            "/users/",
            json={
                "username": "",  # Empty username
                "email": "invalid-email",
                "password": "123",
            },
        )
        assert response.status_code == 422
