"""
Provides CRUD operations for the Product model.
"""

from pydantic import UUID4
from sqlalchemy import Result, Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.structured.product import Product
from app.repositories.base_sql_repository import BaseRepository


class ProductRepository(BaseRepository[Product]):
	"""Repository for performing CRUD operations on SQL Product model."""

	def __init__(self, session: AsyncSession):
		"""
		Initialize the ProductRepository with an async session.

		Args:
			session (AsyncSession): The database session.
		"""
		super().__init__(Product, session)

	async def get(self, _id: UUID4) -> Product | None:
		"""
		Retrieve a Product by their UUID4.

		Args:
			_id (UUID4): The Product's UUID.

		Returns:
			Product | None: The Product instance or None if not found.
		"""
		return await super().get(_id)

	async def delete(self, _id: UUID4) -> bool:
		"""
		Delete a Product by their UUID4.

		Args:
			_id (UUID4): The Product's UUID.

		Returns:
			bool: True if deletion was successful, False otherwise.
		"""
		return await super().delete(_id)

	async def get_by_name(self, name: str) -> Product | None:
		"""
		Retrieve a product by its name.

		Args:
			name (str): The name of the product.

		Returns:
			Product | None: The product if found, otherwise None.
		"""
		stmt: Select = select(self.model).where(self.model.name == name)
		result: Result = await self.session.execute(stmt)
		return result.scalar_one_or_none()
