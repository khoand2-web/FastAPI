# app/routers/order_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.order_service import create_order
from app.schemas.order_schema import OrderCreate, OrderRead
from app.core.security import get_current_user

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/", response_model=OrderRead)
def create_new_order(order_in: OrderCreate, db: Session = Depends(get_db),current_user=Depends(get_current_user)):
    """
    Create an order for current user.
    Note: authentication/authorization is not wired here for brevity.
    """
    
    user_id = current_user.id
   
