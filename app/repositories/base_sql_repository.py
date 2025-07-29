"""
Base repository implementation module in app.repositories.

Provides reusable async CRUD operations for SQLAlchemy ORM models.
"""

from typing import Any
from uuid import UUID

from sqlalchemy import Result, Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.interfaces.repository_interface import IRepository, T


class BaseRepository(IRepository[T]):
	"""
	Base class for async CRUD operations using SQLAlchemy ORM.

	Attributes:
		model (type[T]): The SQLAlchemy model class.
		session (AsyncSession): The async database session.
	"""

	def __init__(self, model: type[T], session: AsyncSession):
		"""
		Initialize the repository with a model and session.

		Args:
			model (type[T]): The SQLAlchemy model.
			session (AsyncSession): The async database session.
		"""
		self.model: type[T] = model
		self.session: AsyncSession = session

	async def get(self, _id: UUID) -> T | None:
		"""
		Retrieve an object by its primary key.

		Args:
			_id (UUID): The primary key of the object.

		Returns:
			T | None: The object if found, otherwise None.
		"""
		stmt: Select = select(self.model).where(self.model.id == _id)  # type: ignore
		result: Result = await self.session.execute(stmt)
		return result.scalar_one_or_none()

	async def get_all(self) -> list[T]:
		"""
		Retrieve all objects of the model type.

		Returns:
			list[T]: A list of all records in the table.
		"""
		stmt: Select[tuple[Any]] = select(self.model)
		result: Result[tuple[Any]] = await self.session.execute(stmt)
		return list(result.scalars().all())

	async def create(self, obj: T) -> T:
		"""
		Insert a new object into the database.

		Args:
			obj (T): The object to be created.

		Returns:
			T: The created object.
		"""
		self.session.add(obj)
		await self.session.flush()
		return obj

	async def update(self, obj: T, new_data: dict[str, Any]) -> T:
		"""
		Update fields of an existing object.

		Args:
			obj (T): The object to update.
			new_data (dict): The fields and values to update.

		Returns:
			T: The updated object.
		"""
		for key, value in new_data.items():
			setattr(obj, key, value)
		self.session.add(obj)
		await self.session.flush()
		return obj

	async def delete(self, _id: UUID) -> bool:
		"""
		Delete an object by its primary key.

		Args:
			_id (UUID): The primary key of the object.

		Returns:
			bool: True if deleted, False otherwise.
		"""
		obj: T | None = await self.get(_id)
		if not obj:
			return False
		await self.session.delete(obj)
		await self.session.flush()
		return True
