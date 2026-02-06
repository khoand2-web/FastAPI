# Testing Guide

## Cài đặt Dependencies

Cài đặt các package cần thiết cho testing:

```bash
pip install -r requirements.txt
```

## Chạy Tests

### Chạy tất cả tests
```bash
pytest
```

### Chạy tests với coverage report
```bash
pytest --cov=app --cov-report=html
```

### Chạy một file test cụ thể
```bash
pytest app/tests/test_auth.py
```

### Chạy một test function cụ thể
```bash
pytest app/tests/test_auth.py::TestLogin::test_login_success
```

### Chạy tests với output chi tiết
```bash
pytest -v -s
```

### Chạy tests với markers
```bash
# Chỉ chạy unit tests
pytest -m unit

# Bỏ qua slow tests
pytest -m "not slow"
```

## Cấu trúc Tests

```
app/tests/
├── conftest.py          # Fixtures và configuration chung
├── test_auth.py         # Tests cho authentication
├── test_users.py        # Tests cho user management
├── test_products.py     # Tests cho product management
└── test_basic.py        # Basic health checks
```

## Fixtures Có Sẵn

### Database & Client
- `db`: SQLite in-memory database session
- `client`: FastAPI TestClient với database test

### Users
- `test_user`: User thường với credentials:
  - Username: `testuser`
  - Password: `testpassword123`
  - Email: `test@example.com`

- `test_superuser`: Superuser với credentials:
  - Username: `admin`
  - Password: `adminpassword123`
  - Email: `admin@example.com`

### Authentication
- `user_token`: JWT token cho test_user
- `superuser_token`: JWT token cho test_superuser
- `auth_headers`: Headers với Bearer token cho test_user
- `superuser_auth_headers`: Headers với Bearer token cho superuser

## Ví Dụ Sử Dụng Fixtures

```python
def test_get_protected_resource(client: TestClient, auth_headers: dict):
    """Test accessing protected endpoint."""
    response = client.get("/api/protected", headers=auth_headers)
    assert response.status_code == 200
```

## Coverage Report

Sau khi chạy tests với coverage, mở file HTML report:

```bash
# Windows
start htmlcov/index.html

# Linux/Mac
open htmlcov/index.html
```

## Best Practices

1. **Tên test rõ ràng**: Sử dụng tên mô tả hành động và kết quả mong đợi
2. **Test isolation**: Mỗi test phải độc lập, không phụ thuộc vào test khác
3. **Sử dụng fixtures**: Tái sử dụng code setup thông qua fixtures
4. **Test cả success và failure cases**: Kiểm tra cả trường hợp thành công và thất bại
5. **Mock external services**: Không gọi API thực hoặc services bên ngoài trong tests

## Continuous Integration

Thêm vào CI/CD pipeline:

```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest --cov=app --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v2
```
