"""
A module for token in the app.schemas.external package.
"""

from datetime import datetime

from pydantic import (
	BaseModel,
	ConfigDict,
	Field,
	field_validator,
)

from app.utils.utils import validate_password


class Token(BaseModel):
	"""
	Token that inherits from Pydantic Base Model.
	"""

	access_token: str = Field(..., description="Access token", min_length=30)
	refresh_token: str = Field(..., description="Refresh token", min_length=30)


class TokenResponse(Token):
	"""
	Token for Response based on Pydantic Base Model.
	"""

	token_type: str = Field(
		default="bearer", title="Token type", description="Type of the token"
	)


class TokenResetPassword(BaseModel):
	"""
	Token Reset Password for Request based on Pydantic Base Model.
	"""

	model_config = ConfigDict(
		json_schema_extra={
			"example": {
				"token": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
				"password": "abcdefg1234567",
			}
		}
	)

	token: str = Field(..., description="Access token", min_length=30)
	password: str = Field(
		...,
		title="New password",
		description="New password to reset",
		validate_default=True,
		min_length=8,
		max_length=14,
	)

	@field_validator("password", mode="before")
	def validate_password(cls, v: str | None) -> str:
		"""
		Validates the password attribute

		Args:
			v (str | None): The password to be validated

		Returns:
			str: The validated password
		"""
		return validate_password(v)


class OAuth2TokenResponse(TokenResponse):
	expire_in: datetime = Field(..., description="Time to expire the token")
	refresh_token: str | None = Field(
		None, description="Refresh token", min_length=30
	)
