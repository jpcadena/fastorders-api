"""
A module for config in the app.config package.
"""

from functools import lru_cache

from app.config.auth_settings import AuthSettings
from app.config.init_settings import InitSettings
from app.config.nosql_db_settings import NoSQLDatabaseSettings
from app.config.settings import Settings
from app.config.sql_db_settings import SQLDBSettings


@lru_cache
def get_sql_db_settings() -> SQLDBSettings:
	"""
	Factory method for getting SQL database settings from environment variables.

	Returns:
		SQLDBSettings: The settings instance.
	"""
	return SQLDBSettings()


@lru_cache
def get_auth_settings() -> AuthSettings:
	"""
	Factory method for getting auth settings from environment variables.

	Returns:
		AuthSettings: The settings instance for authentication.
	"""
	return AuthSettings()


@lru_cache
def get_init_settings() -> InitSettings:
	"""
	Factory method for getting init settings.

	Returns:
		InitSettings: The init settings instance.
	"""
	return InitSettings()


@lru_cache
def get_settings() -> Settings:
	"""
	Factory method for getting settings from environment variables.

	Returns:
		Settings: The settings instance.
	"""
	return Settings()


@lru_cache
def get_nosql_db_settings() -> NoSQLDatabaseSettings:
	"""
	Factory method for getting NoSQL db settings from environment variables.

	Returns:
		NoSQLDatabaseSettings: The NoSQL settings instance.
	"""
	return NoSQLDatabaseSettings()


init_setting: InitSettings = get_init_settings()
setting: Settings = get_settings()
sql_db_setting: SQLDBSettings = get_sql_db_settings()
auth_setting: AuthSettings = get_auth_settings()
nosql_db_settings: NoSQLDatabaseSettings = get_nosql_db_settings()
