# app/tests/test_products.py
"""
Tests cho product management endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.product_model import Product


@pytest.fixture
def test_product(db: Session) -> Product:
    """Tạo product mẫu để test."""
    product = Product(
        name="Test Product",
        description="Test Description",
        price=99.99,
        sku="TEST-001",
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


class TestCreateProduct:
    """Test product creation."""

    def test_create_product_success(self, client: TestClient):
        """Test tạo product mới thành công."""
        response = client.post(
            "/products/",
            json={
                "name": "New Product",
                "description": "Product Description",
                "price": 49.99,
                "sku": "NEW-001",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "New Product"
        assert data["price"] == 49.99
        assert data["sku"] == "NEW-001"

    def test_create_product_without_optional_fields(self, client: TestClient):
        """Test tạo product không có fields optional."""
        response = client.post(
            "/products/",
            json={
                "name": "Simple Product",
                "price": 29.99,
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Simple Product"
        assert data["price"] == 29.99

    def test_create_product_duplicate_sku(self, client: TestClient, test_product: Product):
        """Test tạo product với SKU trùng."""
        response = client.post(
            "/products/",
            json={
                "name": "Another Product",
                "description": "Different product",
                "price": 79.99,
                "sku": test_product.sku,
            },
        )
        # Tùy vào logic của bạn, có thể là 400 hoặc 409
        assert response.status_code in [400, 409]

    def test_create_product_invalid_price(self, client: TestClient):
        """Test tạo product với giá không hợp lệ."""
        response = client.post(
            "/products/",
            json={
                "name": "Invalid Product",
                "price": -10.00,  # Negative price
                "sku": "INVALID-001",
            },
        )
        assert response.status_code in [400, 422]


class TestListProducts:
    """Test listing products."""

    def test_list_products_empty(self, client: TestClient):
        """Test list products khi chưa có product nào."""
        response = client.get("/products/")
        assert response.status_code == 200
        assert response.json() == []

    def test_list_products_with_data(self, client: TestClient, test_product: Product):
        """Test list products khi có dữ liệu."""
        response = client.get("/products/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == test_product.name
        assert data[0]["price"] == test_product.price

    def test_list_products_multiple(self, client: TestClient, db: Session):
        """Test list nhiều products."""
        # Tạo nhiều products
        products = [
            Product(name=f"Product {i}", price=float(i * 10), sku=f"SKU-{i}")
            for i in range(1, 6)
        ]
        for product in products:
            db.add(product)
        db.commit()

        response = client.get("/products/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 5
