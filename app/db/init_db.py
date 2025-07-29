"""
Initialization of the database (PostgreSQL) script
"""

import logging

from app.db.session import async_engine
from app.models.base_class import Base

logger: logging.Logger = logging.getLogger(__name__)


async def init_db() -> None:
	"""
	Initializes the database by dropping all tables and creating them again.

	This is typically used for development or testing environments only.

	Returns:
		NoneType: None
	"""
	try:
		async with async_engine.begin() as conn:
			logger.info("Dropping all tables...")
			await conn.run_sync(Base.metadata.drop_all)
			logger.info("Creating all tables...")
			await conn.run_sync(Base.metadata.create_all)
		logger.info("Database initialized successfully.")
	except Exception as e:
		logger.exception("Error initializing the database: %s", e)
		raise
