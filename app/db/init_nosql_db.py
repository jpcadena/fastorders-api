"""
A module for init NoSQL db in the app.db package.
"""

from collections.abc import Mapping
from typing import Any

from beanie import init_beanie
from pymongo import AsyncMongoClient

from app.config.config import get_nosql_db_settings
from app.models.unstructured import MLModelResult, ProductReview

url: str = str(get_nosql_db_settings.BEANIE_DATABASE_URI)
async_mongo_client: AsyncMongoClient[Mapping[str, Any] | Any] = (
	AsyncMongoClient(url)
)


async def init_nosql_db() -> None:
	"""
	Init connection to MongoDB

	Returns:
		NoneType: None
	"""
	await init_beanie(
		database=async_mongo_client.db_name,
		document_models=[ProductReview, MLModelResult],
	)


async def close_db() -> None:
	"""
	Close connection to MongoDB

	Returns:
		NoneType: None
	"""
	await async_mongo_client.close()
