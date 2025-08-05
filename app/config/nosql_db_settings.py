"""
A module for NoSQL db settings in the app.config package.
"""

from pydantic import MongoDsn, PositiveInt, field_validator
from pydantic_core import MultiHostUrl
from pydantic_core.core_schema import ValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict


class NoSQLDatabaseSettings(BaseSettings):
	"""Settings class for NoSQL database configuration"""

	model_config = SettingsConfigDict(
		env_file=".env",
		env_file_encoding="utf-8",
		case_sensitive=True,
		extra="allow",
	)

	MONGODB_SCHEME: str
	MONGODB_USERNAME: str
	MONGODB_PASSWORD: str
	MONGODB_SERVER: str
	MONGODB_PORT: PositiveInt
	MONGODB_DB: str
	BEANIE_DATABASE_URI: MongoDsn | None = None

	@field_validator("BEANIE_DATABASE_URI", mode="before")
	def assemble_mongodb_connection(
		cls,
		v: str | None,  # noqa: ARG001
		info: ValidationInfo,
	) -> MongoDsn:
		"""
		Assemble the MongoDB connection as URI string

		Args:
			v (str): Variables to consider
			info (ValidationInfo): The field validation info

		Returns:
			MongoDsn: MongoDB URI

		Raises:
			ValueError: If info.config is not set
		"""
		if info.config is None:
			raise ValueError("info.config cannot be None")
		mongo_dsn: MongoDsn = MultiHostUrl.build(
			scheme=info.data.get("MONGODB_SCHEME", ""),
			username=info.data.get("MONGODB_USERNAME"),
			password=info.data.get("MONGODB_PASSWORD"),
			host=info.data.get("MONGODB_SERVER"),
			port=info.data.get("MONGODB_PORT"),
			path=f"/{info.data.get('MONGODB_DB', '')}",
		)
		return mongo_dsn
