from fastapi import FastAPI
from app.database import create_db
from app.routers import products, users, auth

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db()

app.include_router(products.router)
app.include_router(users.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "API is running!"}
