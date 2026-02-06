from sqlalchemy.ext.asyncio import AsyncSession
from app.models.order_item_model import OrderItem


class OrderItemRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, item: OrderItem):
        self.db.add(item)
