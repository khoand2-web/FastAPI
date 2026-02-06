# Web Bán Hàng – FastAPI

Dự án backend **Web bán hàng** được xây dựng bằng **FastAPI**, sử dụng **PostgreSQL**, **SQLAlchemy**, **Alembic**, JWT Authentication và cấu trúc nhiều layer (router / service / repository).

---

## 1. Yêu cầu hệ thống

* Python **>= 3.10**
* pip
* PostgreSQL (khuyến nghị cho production)
* Git

---

## VAI TRÒ TRONG HỆ THỐNG
* USER (người dùng)
 - đăng ký và đăng nhập tài khoản
 - xem danh sách và chi tiết sản phẩm
 - thêm sản phẩm vào giỏ hàng
 - tạo đơn hàng từ giỏ hàng
 - xem lịch sử đơn hàng của bản thân
* ADMIN (quản trị)
 - quản lý danh mục sản phẩm (category)
 - quản lý sản phẩm
 - xem và quản lý đơn hàng của người dùng
 - cập nhật trạng thái đơn hàng

---

## CÁC MODULE CHỨC NĂNG CHÍNH 

---

** Authentication (xác thực và phân quyền)

* Chức năng
- đăng ký tài khoản
- đăng nhập và nhận access token
- xác thực người dùng thông qua jwt
- phân quyền user / admin

* Luồng đăng nhập
- người dùng gửi username và password
- hệ thống xác thực thông tin đăng nhập
- sinh jwt access token
- token được sử dụng cho các API yêu cầu xác thực 

----

** USER 
Module quản lý thông tin người dùng trong hệ thống 

* chức năng
- lưu trữ thông tin tài khoản người dùng
- quản lý vai trò (user / admin)
- liên hết với giỏ hàng và đơn hàng

---

** CATEGORY
Danh mục được sử dụng để phân loại sản phẩm

* Chức năng 
- Admin : Tạo, cập nhật, xóa danh mục 
- User : xem danh sách danh mục 

* Mục đích 
- giúp tổ chức sản phẩm rõ ràng 
- hỗ trợ việc quản lý mở rộng sản phẩm 

---

** PRODUCT (sản phẩm)
Module quản lý sản phẩm được bán trong hệ thống

* Chức năng 
- Admin:
 + Tạo, cập nhật, xóa sản phẩm
 + giá sản phẩm vào danh mục 
- User:
 + xem danh sách sản phẩm
 + xem chi tiết mô tả sản phẩm

* Thông tin sản phẩm
- tên sản phẩm
- giá
- mô tả sản phẩm
- số lượng tồn kho
- danh mục 

 ---

** CART (giỏ hàng cho người dùng)
Giỏ hàng cho phép người dùng lưu trữ sản phẩm trước khi đặt hàng

* chức năng
- thêm sản giỏ hàng
- cập nhật số lượng sản phẩm trong giỏ
- xóa sản phẩm khỏi giỏ hàng
- mỗi user chỉ có một giỏ hàng riêng

* Mục đích
- hỗ trợ quá trình mua sắm 
- chuẩn bị dữ liệu cho bước đặt hàng

---

** ORDER
Module xử lý nghiệp vụ đăt hàng

* chức năng
- User:
 + tạo đơn hàng từ giỏ hàng
 + xem danh sách đơn hàng của bản thân
- Admin:
 + xem tất cả đơn hàng
 + cập nhật trạng thái đơn hàng

* Luồng đặt hàng
- user thêm sản phẩm vào giỏ hàng
- user thực hiện chechout
- hệ thống tạo order và order items
- admin xử lý và cập nhật trạng thái đơn hàng

---

## 2. Cấu trúc thư mục (tóm tắt)

```
app/
├── main.py              # Entry point của FastAPI
├── core/                # Config, security, settings
├── models/              # SQLAlchemy models
├── schemas/             # Pydantic schemas
├── repositories/        # Tầng thao tác DB
├── services/            # Tầng xử lý business logic
├── routers/             # API routes
├── db/                  # Database session, base
└── utils/               # Helper functions

---

## 3. Setup & Deploy local server

### Bước 1: Clone project

- bash
git clone <repo_url>
cd <project_folder>


---

### Bước 2: Tạo và kích hoạt virtual environment

**Windows**

- bash
python -m venv venv
venv\Scripts\activate


**MacOS / Linux**

- bash
python3 -m venv venv
source venv/bin/activate


---

### Bước 3: Cài đặt dependencies

- bash
pip install -r requirements.txt


---

### Bước 4: Cấu hình biến môi trường

Copy file mẫu:

- bash
cp .env.example .env


Ví dụ `.env`:

- env
DATABASE_URL=postgresql+psycopg://postgres:password@localhost:5432/web_ban_hang
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30


---

### Bước 5: Chạy migration database

- bash
alembic upgrade head


---

### Bước 6: Chạy server local

- bash
uvicorn app.main:app --reload


Server sẽ chạy tại:

```
http://127.0.0.1:8000
```

---

## 4. Swagger & API Documentation

FastAPI tự động sinh tài liệu API.

### Swagger UI

```
http://127.0.0.1:8000/docs
```

* Test trực tiếp API
* Gửi request (GET / POST / PUT / DELETE)
* Test JWT Authorization (Authorize)

### ReDoc

```
http://127.0.0.1:8000/redoc
```

---

## 5. Test API

### 5.1 Test bằng Swagger

1. Mở `/docs`
2. Đăng nhập để lấy **access token**
3. Click **Authorize** → nhập:

```
Bearer <access_token>
```

4. Test các API protected

---

### 5.2 Test bằng pytest

```bash
pytest
```

---

## 6. Database

* Mặc định: **PostgreSQL**
* ORM: **SQLAlchemy 2.0**
* Migration: **Alembic**

Quan hệ chính:

* User
* Product
* Cart / CartItem
* Order / OrderItem

---

## 7. Auth & Security

* JWT Authentication
* OAuth2 Password Flow
* Password hashing: `passlib[bcrypt]`

---

## 8. Ghi chú cho developer

* Router chỉ xử lý request/response
* Service xử lý business logic
* Repository chỉ thao tác DB
* Schema dùng để validate & serialize data

---

## 9. License

MIT License
