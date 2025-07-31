"""
A module for config in the app.config package.
"""

from functools import lru_cache

from app.config.auth_settings import AuthSettings
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
