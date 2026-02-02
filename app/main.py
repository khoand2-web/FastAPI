# app/main.py
from fastapi import FastAPI
from app.core.config import settings
from app.core.logging_config import configure_logging
from app.db.init_db import init_db
from app.middleware.cors import add_cors
from app.middleware.error_handler import register_error_handlers
from contextlib import asynccontextmanager
from app.routers import auth_router, user_router, product_router, order_router, cart_router  # type: ignore

configure_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db
    yield

app = FastAPI(
    title="FastAPI VMO",
    version="0.1.0",
    debug=settings.DEBUG,
    lifespan=lifespan
)


# include middleware
add_cors(app)
register_error_handlers(app)

# include routers
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(product_router)
app.include_router(order_router)
app.include_router(cart_router)