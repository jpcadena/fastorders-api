"""
Provides CRUD operations for the Order model.
"""

from pydantic import UUID4
from sqlalchemy import Result, Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.structured.order import Order
from app.repositories.base_sql_repository import BaseRepository


class OrderRepository(BaseRepository[Order]):
	"""Repository for performing CRUD operations on Order model."""

	def __init__(self, session: AsyncSession):
		"""
		Initialize the OrderRepository with an async session.

		Args:
			session (AsyncSession): The database session.
		"""
		super().__init__(Order, session)

	async def get(self, _id: UUID4) -> Order | None:
		"""
		Retrieve an Order by their UUID4.

		Args:
			_id (UUID4): The Order's UUID.

		Returns:
			Order | None: The Order instance or None if not found.
		"""
		return await super().get(_id)

	async def delete(self, _id: UUID4) -> bool:
		"""
		Delete an Order by their UUID4.

		Args:
			_id (UUID4): The Order's UUID.

		Returns:
			bool: True if deletion was successful, False otherwise.
		"""
		return await super().delete(_id)

	async def get_by_user_id(self, user_id: UUID4) -> list[Order]:
		"""
		Retrieve all orders made by a specific user.

		Args:
			user_id (UUID4): The ID of the user.

		Returns:
			list[Order]: A list of orders placed by the user.
		"""
		stmt: Select = select(self.model).where(self.model.user_id == user_id)
		result: Result = await self.session.execute(stmt)
		return list(result.scalars().all())
