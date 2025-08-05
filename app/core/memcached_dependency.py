"""
A module for memcached dependency in the app.core package.
"""

import logging
from typing import Annotated, Any

from bmemcached import Client
from fastapi import Depends
from pydantic import PositiveInt

from app.config.auth_settings import AuthSettings
from app.config.config import get_auth_settings

logger: logging.Logger = logging.getLogger(__name__)


class MemcachedDependency:
	"""A class to handle Memcached connections as a FastAPI dependency."""

	def __init__(self) -> None:
		_auth_settings: AuthSettings = get_auth_settings()
		host: str = _auth_settings.MEMCACHED_HOST
		port: PositiveInt = _auth_settings.MEMCACHED_PORT
		servers: list[str] = [
			f"{host}:{port}",
		]
		username: str = _auth_settings.MEMCACHED_USERNAME
		password: str = _auth_settings.MEMCACHED_PASSWORD
		self._memcached: Client = Client(
			servers=servers, username=username, password=password
		)
		self._memcached.enable_retry_delay(True)

	def __enter__(self) -> Client:
		return self._memcached

	def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
		self._memcached.disconnect_all()

	def get_client(self) -> Client:
		"""
		Get the Memcached client

		Returns:
			Client: The Memcached client
		"""
		return self._memcached


async def get_memcached_dep(
	memcached_dependency: Annotated[MemcachedDependency, Depends()],
) -> Client:
	"""
	Dependency to provide a Memcached client.

	Args:
		memcached_dependency (MemcachedDependency): The dependency to provide the Memcached

	Returns:
		Client: The Memcached client
	"""
	return memcached_dependency.get_client()
