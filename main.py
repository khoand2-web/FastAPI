from fastapi import FastAPI
from routers import products, users
from database import create_db

app = FastAPI(title="Shop Online FastAPI")

# Tạo database + tables
create_db()

# Thêm router Products + Users
app.include_router(products.router)
app.include_router(users.router)

@app.get("/")
def home():
    return {"message": "Welcome to FastAPI Shop!"}
