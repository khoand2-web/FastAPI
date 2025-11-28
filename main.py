from fastapi import FastAPI
from database import create_db
from routers import products, auth, users

app = FastAPI(title="Shop Online FastAPI")

# ---------------------------------------------------
# Tạo database khi server khởi động
# ---------------------------------------------------
@app.on_event("startup")
def on_startup():
    create_db()


# ---------------------------------------------------
# Đăng ký router
# ---------------------------------------------------
app.include_router(auth.router)      # /auth/login, /auth/register
app.include_router(products.router)  # /products CRUD
app.include_router(users.router)     # /users/me, /users/{id}


# ---------------------------------------------------
# Home endpoint
# ---------------------------------------------------
@app.get("/")
def home():
    return {"message": "Welcome to FastAPI Shop!"}
