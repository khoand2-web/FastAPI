from .auth_router import router as auth_router
from .users_router import router as user_router
from .products_router import router as product_router
from .order_router import router as order_router
from .cart_router import router as cart_router
__all__ = [
    "auth_router",
    "user_router",
    "product_router",
    "order_router",
    "cart_router",
]
