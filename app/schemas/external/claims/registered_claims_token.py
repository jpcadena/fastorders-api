"""
A module for registered claims token in the app.schemas.external.claims package.
"""

import http
import re
from typing import Literal
from uuid import uuid4

from pydantic import (
	UUID4,
	AnyHttpUrl,
	AnyUrl,
	BaseModel,
	Field,
	NonNegativeInt,
	field_validator,
)

from app.config.config import auth_setting
from app.core.enums.toke_type import TokenType
from app.exceptions.exceptions import ServiceException


class RegisteredClaimsToken(BaseModel):
	"""
	Registered Claims Token class based on Pydantic Base Model with
	Registered claims.
	"""

	iss: AnyUrl | None = Field(
		default=auth_setting.SERVER_URL,
		title="Issuer",
		description="Principal that issued JWT as HTTP URL",
	)
	sub: str = Field(
		...,
		title="Subject",
		description="Subject of JWT starting with username: followed"
		" by User ID",
		validate_default=True,
		min_length=45,
		max_length=45,
	)
	aud: str | None = Field(
		default=f"{auth_setting.AUDIENCE}",
		title="Audience",
		description="Recipient of JWT",
		min_length=1,
	)
	exp: NonNegativeInt = Field(
		...,
		title="Expiration time",
		description="Expiration time on or after which the JWT MUST NOT be"
		" accepted for processing",
	)
	nbf: NonNegativeInt = Field(
		...,
		title="Not Before",
		description="Time Before which the JWT MUST NOT be accepted for "
		"processing",
	)
	iat: NonNegativeInt = Field(
		..., title="Issued At", description="Time at which the JWT was issued"
	)
	jti: UUID4 | None = Field(
		default_factory=uuid4,
		title="JWT ID",
		description="Unique Identifier for the JWT",
	)
	sid: UUID4 | None = Field(
		default_factory=uuid4,
		title="Session ID",
		description="Session ID",
	)
	scope: TokenType | None = Field(
		default=TokenType.ACCESS_TOKEN,
		title="Token type",
		description="Token type value",
	)
	at_use_nbr: int = Field(
		default=auth_setting.MAX_REQUESTS,
		title="Number of requests",
		description="Number of API requests for which the access token can be"
		" used",
		gt=0,
		le=30,
	)
	nationalities: list[str] | None = Field(
		default=["ECU"],
		title="Nationalities",
		description="String array representing the End-User's nationalities",
		min_length=1,
		max_length=200,
	)
	htm: Literal["POST"] | None = http.HTTPMethod.POST.value
	htu: AnyHttpUrl | None = Field(
		default=AnyHttpUrl(
			f"{auth_setting.SERVER_URL}{auth_setting.TOKEN_URL}",
		),
		title="HTTP URI",
		description="The HTTP URI of the request",
	)

	@field_validator("sub", mode="before")
	def username_starts_with_non_zero(cls, v: str | None) -> str:
		"""
		Validate that the username starts with a non-zero

		Args:
			v (str | None): The sub value

		Returns:
			str: The validated sub attribute

		Raises:
			ValueError: If the sub attribute is invalid
			ServiceException: If the sub attribute is empty
		"""
		if not v:
			raise ServiceException("sub is empty")
		if re.match(auth_setting.SUB_REGEX, v):
			return v
		raise ValueError(
			"sub must start with 'username:' followed by non-zero digits"
		)
