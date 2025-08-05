"""
A module for public claims token in the app.schemas.external.claims package.
"""

from pydantic import (
	BaseModel,
	EmailStr,
	Field,
)


class PublicClaimsToken(BaseModel):
	"""
	Token class based on Pydantic Base Model with Public claims (IANA).
	"""

	email: EmailStr = Field(
		...,
		title="Email",
		description="Preferred e-mail address of the User",
	)
	nickname: str = Field(
		...,
		title="Casual name",
		description="Casual name of the User (First Name)",
		min_length=1,
		max_length=50,
	)
	preferred_username: str = Field(
		...,
		title="Preferred username",
		description="Shorthand name by which the End-User wishes to be "
		"referred to (Username)",
		min_length=1,
		max_length=50,
	)
