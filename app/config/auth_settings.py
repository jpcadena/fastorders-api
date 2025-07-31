"""
A module for auth settings in the app.config package.
"""

from typing import Final

from pydantic import AnyHttpUrl, PositiveInt, field_validator
from pydantic_core import MultiHostUrl
from pydantic_core.core_schema import ValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict


class AuthSettings(BaseSettings):
	"""Settings class for authentication using JWT and Memcached"""

	model_config = SettingsConfigDict(
		env_file=".env",
		env_file_encoding="utf-8",
		case_sensitive=True,
		extra="allow",
	)

	MAX_REQUESTS: Final[PositiveInt] = 30
	RATE_LIMIT_DURATION: Final[PositiveInt] = 60
	BLACKLIST_EXPIRATION_SECONDS: Final[PositiveInt] = 3600
	API_V1_STR: Final[str] = "/api/v1"
	ALGORITHM: Final[str] = "HS256"
	AUTH_URL: Final[str] = "api/v1/auth/"
	TOKEN_URL: Final[str] = "api/v1/auth/login"
	OAUTH2_SCHEME: Final[str] = "JWT"
	OAUTH2_TOKEN_DESCRIPTION: Final[str] = (
		"JWT token used to authenticate most of the API endpoints."
	)
	OAUTH2_REFRESH_TOKEN_DESCRIPTION: Final[str] = (
		"JWT token used to authenticate most of he API endpoints."
	)
	TOKEN_USER_INFO_REGEX: Final[str] = (
		r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-"
		r"[0-9a-f]{4}-[0-9a-f]{12}:\d{1,3}\."
		r"\d{1,3}\.\d{1,3}\.\d{1,3}$"
	)
	SUB_REGEX: Final[str] = (
		r"^username:[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-"
		r"[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
	)
	HEADERS: dict[str, str] = {"WWW-Authenticate": "Bearer"}
	DETAIL: Final[str] = "Could not validate credentials"
	NO_CLIENT_FOUND: Final[str] = "No client found on the request"
	CACHE_SECONDS: Final[PositiveInt] = 3600
	CERTIFICATE_TRANSPARENCY_MAX_AGE: Final[PositiveInt] = 86400  # seconds

	SECRET_KEY: str
	SERVER_URL: AnyHttpUrl
	SERVER_DESCRIPTION: str
	ACCESS_TOKEN_EXPIRE_MINUTES: float
	REFRESH_TOKEN_EXPIRE_MINUTES: PositiveInt
	EMAIL_RESET_TOKEN_EXPIRE_HOURS: PositiveInt
	AUDIENCE: AnyHttpUrl | None = None
	STRICT_TRANSPORT_SECURITY_MAX_AGE: PositiveInt
	SWAGGER_SHA_KEY: str

	MEMCACHED_HOST: str
	MEMCACHED_PORT: PositiveInt
	MEMCACHED_USERNAME: str
	MEMCACHED_PASSWORD: str
	MEMCACHED_URI: MultiHostUrl | None = None

	@field_validator("MEMCACHED_URI", mode="before")
	def assemble_memcached_connection(
		cls,
		v: str | None,  # noqa: ARG001
		info: ValidationInfo,
	) -> MultiHostUrl:
		"""
		Assemble the cache database connection as URI string

		Args:
			v (str | None): Variables to consider. Default to MEMCACHED_URI
			info (ValidationInfo): The field validation info

		Returns:
			MultiHostUrl: The Memcached URI

		Raises:
			ValueError: If MEMCACHED_URI is invalid
		"""
		if info.config is None:
			raise ValueError("info.config cannot be None")
		return MultiHostUrl.build(
			scheme="memcached",
			username=info.data.get("MEMCACHED_USERNAME"),
			password=info.data.get("MEMCACHED_PASSWORD"),
			host=info.data.get("MEMCACHED_HOST", ""),
			port=info.data.get("MEMCACHED_PORT"),
		)

	@field_validator("AUDIENCE", mode="before")
	def assemble_audience(
		cls,
		v: str | None,  # noqa: ARG001
		info: ValidationInfo,
	) -> AnyHttpUrl:
		"""
		Combine server host and API_V1_STR to create the audience string.

		Args:
			v (str | None): The value of audience attribute. Default to AUDIENCE
			info (ValidationInfo): The field validation info

		Returns:
			AnyHttpUrl: The AUDIENCE attribute

		Raises:
			ValueError: If AUDIENCE is invalid
		"""
		if info.config is None:
			raise ValueError("info.config cannot be None")
		return AnyHttpUrl(
			f"{str(info.data.get('SERVER_URL'))[:-1]}:8000/"
			f"{info.data.get('TOKEN_URL')}"
		)
