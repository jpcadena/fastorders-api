"""
A module for settings in the app.config package.
"""

from typing import Any

from pydantic import (
	AnyHttpUrl,
	EmailStr,
	IPvAnyAddress,
	PositiveInt,
	field_validator,
)
from pydantic_core.core_schema import ValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
	"""Settings class based on Pydantic Base Settings"""

	model_config = SettingsConfigDict(
		env_file=".env",
		env_file_encoding="utf-8",
		case_sensitive=True,
		extra="allow",
	)

	HOST: IPvAnyAddress
	PORT: PositiveInt
	SERVER_RELOAD: bool
	SERVER_LOG_LEVEL: str
	RESEND_API_KEY: str
	EMAIL_SUBJECT: str
	EMAILS_FROM_EMAIL: EmailStr | None = None
	EMAILS_FROM_NAME: str | None = None
	BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []

	@field_validator("BACKEND_CORS_ORIGINS", mode="before")
	def assemble_cors_origins(
		cls,
		v: str | list[str],
	) -> list[str] | str:
		"""
		Assemble a list of allowed CORS origins.

		:param v: Provided CORS origins, either a string or a list of
		strings
		:type v: Union[str, list[str]]
		:return: List of Backend CORS origins to be accepted
		:rtype: Union[list[str], str]
		"""
		if isinstance(v, str) and not v.startswith("["):
			return [i.strip() for i in v.split(",")]
		if isinstance(v, list):
			return v
		raise ValueError(v)

	CONTACT_NAME: str | None = None
	CONTACT_URL: AnyHttpUrl | None = None
	CONTACT_EMAIL: EmailStr | None = None
	CONTACT: dict[str, Any] | None = None

	@field_validator("CONTACT", mode="before")
	def assemble_contact(
		cls,
		v: str | None,  # noqa: ARG001
		info: ValidationInfo,
	) -> dict[str, str]:
		"""
		Assemble contact information

		:param v: Variables to consider
		:type v: str
		:param info: The field validation info
		:type info: ValidationInfo
		:return: The contact attribute
		:rtype: dict[str, str]
		"""
		if info.config is None:
			raise ValueError("info.config cannot be None")
		contact: dict[str, Any] = {}
		if info.data.get("CONTACT_NAME"):
			contact["name"] = info.data.get("CONTACT_NAME")
		if info.data.get("CONTACT_URL"):
			contact["url"] = info.data.get("CONTACT_URL")
		if info.data.get("CONTACT_EMAIL"):
			contact["email"] = info.data.get("CONTACT_EMAIL")
		return contact
