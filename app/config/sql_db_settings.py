"""
A module for SQL db settings in the app.config package.
"""

from pydantic import PositiveInt, PostgresDsn, field_validator
from pydantic_core import MultiHostUrl
from pydantic_core.core_schema import ValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict


class SQLDBSettings(BaseSettings):
	"""SQLDB settings class"""

	model_config = SettingsConfigDict(
		env_file=".env",
		env_file_encoding="utf-8",
		case_sensitive=True,
		extra="allow",
	)
	POSTGRES_SCHEME: str
	POSTGRES_USER: str
	POSTGRES_PASSWORD: str
	POSTGRES_HOST: str
	POSTGRES_PORT: PositiveInt
	POSTGRES_DB: str
	DATABASE_URL: PostgresDsn | None = None

	@field_validator("DATABASE_URL", mode="before")
	def assemble_postgres_dsn(
		cls,
		v: str | None,  # noqa: ARG001
		info: ValidationInfo,
	) -> PostgresDsn:
		"""
		Assembles the database connection string from environment variables.

		Args:
			v (str | None): The database connection string.
			info (ValidationInfo): The validation info instance.

		Returns:
			PostgresDsn: The validated database connection string.
		"""
		multi_host_url: MultiHostUrl = MultiHostUrl.build(
			scheme=info.data.get("POSTGRES_SCHEME"),
			username=info.data.get("POSTGRES_USER"),
			password=info.data.get("POSTGRES_PASSWORD"),
			host=info.data.get("POSTGRES_HOST"),
			port=info.data.get("POSTGRES_PORT"),
			path=info.data.get("POSTGRES_DB"),
		)
		return PostgresDsn(f"{multi_host_url}")
