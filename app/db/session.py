"""
Database session script
"""

import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
	AsyncEngine,
	AsyncSession,
	async_sessionmaker,
	create_async_engine,
)

from app.config.sql_db_settings import get_sql_db_settings

logger: logging.Logger = logging.getLogger(__name__)

url: str = f"{get_sql_db_settings().DATABASE_URL}"

async_engine: AsyncEngine = create_async_engine(
	url,
	pool_pre_ping=True,
	future=True,
	echo=True,
	pool_size=10,
	max_overflow=20,
)

AsyncSessionLocal = async_sessionmaker(
	bind=async_engine,
	autoflush=False,
	expire_on_commit=False,
	class_=AsyncSession,
)


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession]:
	"""
	Yield an asynchronous session to the database.

	Yields:
		AsyncGenerator[AsyncSession]: The session yielded.

	Raises:
		Exception: If the database connection fails.
	"""
	async with AsyncSessionLocal() as session:
		try:
			yield session
			await session.commit()
		except Exception as e:
			logger.error("Session rollback due to exception: %s", e)
			await session.rollback()
			raise


async def check_db_health(session: AsyncSession) -> bool:
	"""
	Check the health of the database connection.

	Args:
		session (AsyncSession): The SQLAlchemy asynchronous session object used to interact with the database.

	Returns:
		bool: True if the database connection is healthy, False otherwise.

	Raises:
		SQLAlchemyError: If the database connection fails.
	"""
	try:
		await session.execute(text("SELECT 1"))
		return True
	except SQLAlchemyError as e:
		logger.error("Database connection error: %s", e)
		return False
