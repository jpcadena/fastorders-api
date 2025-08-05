"""
This module provides API dependencies that can be used across
multiple routes and modules.
It includes authentication utilities, connection handlers for external
services like Memcached, and factory functions for service classes.
"""

import logging
from collections.abc import Generator
from contextlib import contextmanager
from typing import Annotated, Any

from bmemcached import Client
from bmemcached.exceptions import MemcachedException
from fastapi import Depends
from pydantic import PositiveInt

from app.config.auth_settings import AuthSettings
from app.core.memcached_dependency import MemcachedDependency

logger: logging.Logger = logging.getLogger(__name__)


class MemcachedConnectionManager:
	"""Memcached connection manager class"""

	def __init__(self, auth_settings: AuthSettings):
		self.__host: str = auth_settings.MEMCACHED_HOST
		self.__port: PositiveInt = auth_settings.MEMCACHED_PORT
		self.__username: str = auth_settings.MEMCACHED_USERNAME
		self.__password: str = auth_settings.MEMCACHED_PASSWORD
		self._client: Client | None = None

	def __start(self) -> None:
		"""
		Start the Memcached client connection

		Returns:
			NoneType: None
		"""
		self._client = Client(
			[
				f"{self.__host}:{self.__port}",
			],
			username=self.__username,
			password=self.__password,
		)
		logger.info("Memcached Database initialized")

	def __stop(self) -> None:
		"""
		Stops the Memcached connection

		Returns:
			NoneType: None
		"""
		if self._client:
			self._client.disconnect_all()

	def get_connection(self) -> Client | None:
		"""
		Get the connection

		Returns:
			Client | None: The connection to the Memcached server if it's available
		"""
		return self._client

	@contextmanager
	def connection(self) -> Generator[Client, Any]:
		"""
		Synchronously get the connection from the client context manager

		Yields:
			Generator[Client, Any, None]: The generator object
		"""
		self.__start()
		try:
			yield self._client
		finally:
			self.__stop()


def get_memcached_dep(
	memcached_dependency: Annotated[MemcachedDependency, Depends()],
) -> Generator[Client]:
	"""
	Lazy generation of Memcached dependency

	Args:
		memcached_dependency (MemcachedDependency): The dependency injection on Memcached

	Yields:
		Generator[Client, None, None]: The Memcached connection instance as a generator object
	"""
	with memcached_dependency as memcached:
		yield memcached


async def check_memcached_health(memcached: Client) -> bool:
	"""
	Check the health of the Memcached connection.

	Args:
		memcached (Client): The Memcached client object used to interact with the Memcached server.

	Returns:
		bool: True if the Memcached connection is healthy, False otherwise.

	Raises:
		MemcachedException: If the Memcached connection is not healthy.
	"""
	try:
		memcached.set(b"health_check", b"ok")
		value = memcached.get(b"health_check")
		if value != b"ok":
			logger.error("Memcached connection error: Invalid value returned")
			return False
		return True
	except MemcachedException as e:
		logger.error(f"Memcached connection error: {e}")
		return False
