"""
Provides CRUD operations for the User model.
"""

from pydantic import UUID4
from sqlalchemy import Result, Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.structured.user import User
from app.repositories.base_sql_repository import BaseRepository


class UserRepository(BaseRepository[User]):
	"""Repository for performing CRUD operations on SQL User model."""

	def __init__(self, session: AsyncSession):
		"""
		Initialize the UserRepository with an async session.

		Args:
			session (AsyncSession): The database session.
		"""
		super().__init__(User, session)

	async def get(self, _id: UUID4) -> User | None:
		"""
		Retrieve a User by their UUID4.

		Args:
			_id (UUID4): The User's UUID.

		Returns:
			User | None: The User instance or None if not found.
		"""
		return await super().get(_id)

	async def delete(self, _id: UUID4) -> bool:
		"""
		Delete a User by their UUID4.

		Args:
			_id (UUID4): The User's UUID.

		Returns:
			bool: True if deletion was successful, False otherwise.
		"""
		return await super().delete(_id)

	async def get_by_username(self, username: str) -> User | None:
		"""
		Retrieve a User by their username.

		Args:
			username (str): The User's username.

		Returns:
			User | None: The user if found, otherwise None.
		"""
		stmt: Select = select(self.model).where(self.model.username == username)
		result: Result = await self.session.execute(stmt)
		return result.scalar_one_or_none()
