"""
Provides CRUD operations for the OrderItem model.
"""

from pydantic import UUID4
from sqlalchemy import Result, Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.structured.order_item import OrderItem
from app.repositories.base_sql_repository import BaseRepository


class OrderItemRepository(BaseRepository[OrderItem]):
	"""Repository for performing CRUD operations on OrderItem model."""

	def __init__(self, session: AsyncSession):
		"""
		Initialize the OrderItemRepository with an async session.

		Args:
			session (AsyncSession): The database session.
		"""
		super().__init__(OrderItem, session)

	async def get(self, _id: UUID4) -> OrderItem | None:
		"""
		Retrieve an Order Item by their UUID4.

		Args:
			_id (UUID4): The Order Item's UUID.

		Returns:
			Order Item | None: The Order Item instance or None if not found.
		"""
		return await super().get(_id)

	async def delete(self, _id: UUID4) -> bool:
		"""
		Delete an Order Item by their UUID4.

		Args:
			_id (UUID4): The Order Item's UUID.

		Returns:
			bool: True if deletion was successful, False otherwise.
		"""
		return await super().delete(_id)

	async def get_items_for_order_id(self, order_id: UUID4) -> list[OrderItem]:
		"""
		Retrieve all items associated with a specific order.

		Args:
			order_id (UUID4): The ID of the order.

		Returns:
			list[OrderItem]: A list of order items.
		"""
		stmt: Select = select(self.model).where(self.model.order_id == order_id)
		result: Result = await self.session.execute(stmt)
		return list(result.scalars().all())
