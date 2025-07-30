"""
Pydantic schemas for User used in requests and responses.
"""

from datetime import date, datetime
from uuid import UUID

from pydantic import (
	BaseModel,
	ConfigDict,
	EmailStr,
	Field,
	PastDate,
	field_validator,
)
from pydantic_extra_types.phone_numbers import PhoneNumber

from app.core.enums.gender import Gender
from app.utils.utils import validate_password


class UserBase(BaseModel):
	"""Base schema for user with common attributes."""

	username: str = Field(
		...,
		title="Username",
		min_length=4,
		max_length=15,
		description="Unique username used for login and identification.",
		examples=["juanp123"],
	)
	email: EmailStr = Field(
		...,
		title="Email address",
		min_length=3,
		max_length=320,
		description="Email used for contact and authentication.",
		examples=["example@mail.com"],
	)
	first_name: str = Field(
		...,
		title="First name",
		min_length=1,
		max_length=50,
		description="User's given name(s).",
		examples=["Juan Pablo"],
	)
	last_name: str = Field(
		...,
		title="Last name",
		min_length=1,
		max_length=100,
		description="User's family name(s).",
		examples=["Cadena Aguilar"],
	)
	gender: Gender | None = Field(
		default=None,
		title="Gender",
		description="Optional gender selection from a predefined set.",
		examples=[Gender.MALE, Gender.FEMALE, Gender.OTHER],
	)
	birthdate: PastDate | None = Field(
		default=None,
		title="Birthdate",
		description="Optional date of birth (must be in the past) in YYYY-MM-DD format.",
		examples=["1993-08-24"],
	)
	phone_number: PhoneNumber | None = Field(
		default=None,
		title="Phone number",
		description="Optional phone number in tel URI format.",
		examples=[str(PhoneNumber("+593987654321"))],
	)


class UserCreate(UserBase):
	"""Schema for creating a new user."""

	model_config = ConfigDict(from_attributes=True)

	password: str = Field(
		...,
		title="Password",
		min_length=8,
		max_length=16,
		description="User's password",
	)

	@field_validator("password", mode="before")
	def validate_password(cls, v: str | None) -> str:
		"""
		Validates the password attribute

		Args:
			v (str | None): Password attribute

		Returns:
			str: The validated password
		"""
		return validate_password(v)


class UserUpdate(BaseModel):
	"""Schema for updating user details."""

	first_name: str | None = Field(
		default=None,
		title="First name",
		min_length=1,
		max_length=50,
		description="Updated first name.",
	)
	last_name: str | None = Field(
		default=None,
		title="Last name",
		min_length=1,
		max_length=100,
		description="Updated last name.",
	)
	gender: Gender | None = Field(
		default=None, title="Gender", description="Updated gender."
	)
	birthdate: date | None = Field(
		default=None, title="Birthdate", description="Updated birthdate."
	)
	phone_number: PhoneNumber | None = Field(
		default=None, title="Phone number", description="Updated phone number."
	)
	is_active: bool | None = Field(
		default=None,
		title="Is active",
		description="Toggle to deactivate or reactivate the user.",
	)


class UserResponse(UserBase):
	"""Schema for returning user details in responses."""

	model_config = ConfigDict(from_attributes=True)

	id: UUID = Field(
		..., title="User ID", description="Unique UUID assigned to the user."
	)
	is_active: bool = Field(
		...,
		title="Is active",
		description="Whether the user account is active.",
	)
	is_superuser: bool = Field(
		...,
		title="Is superuser",
		description="Whether the user has elevated (admin) privileges.",
	)
	created_at: datetime = Field(
		...,
		title="Created at",
		description="Datetime when the user was created.",
	)
	updated_at: datetime | None = Field(
		default=None,
		title="Updated at",
		description="Datetime of the most recent update, if any.",
	)
