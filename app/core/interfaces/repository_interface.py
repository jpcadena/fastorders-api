"""
Repository interface module in app.core.interfaces.

Defines an abstract base class for CRUD operations using SQLAlchemy models.
"""

from abc import ABC, abstractmethod
from typing import Any, TypeVar

from app.models.base_class import Base

T = TypeVar("T", bound=Base)


class IRepository[T: Base](ABC):
	"""
	Abstract base class for CRUD repository interfaces.

	This interface enforces the basic operations (Create, Read, Update, Delete)
	for interacting with SQLAlchemy ORM models.
	"""

	@abstractmethod
	async def get(self, _id: str) -> T | None:
		"""
		Retrieve an object by its ID.

		Args:
			_id (str): The primary key of the object.

		Returns:
			T | None: The found object or None if not found.
		"""

	@abstractmethod
	async def get_all(self) -> list[T]:
		"""
		Retrieve all records of this type.

		Returns:
			list[T]: A list of all objects.
		"""

	@abstractmethod
	async def create(self, obj: T) -> T:
		"""
		Insert a new object into the database.

		Args:
			obj (T): The object to be created.

		Returns:
			T: The newly created object.
		"""

	@abstractmethod
	async def update(self, obj: T, new_data: dict[str, Any]) -> T:
		"""
		Update an existing object with new data.

		Args:
			obj (T): The original object.
			new_data (dict): Fields to update.

		Returns:
			T: The updated object.
		"""

	@abstractmethod
	async def delete(self, _id: str) -> bool:
		"""
		Delete an object by its ID.

		Args:
			_id (str): The primary key of the object to delete.

		Returns:
			bool: True if deletion was successful, False otherwise.
		"""
