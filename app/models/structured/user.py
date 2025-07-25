"""
A module for user in the app.models package.
"""

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import UUID4, EmailStr, PastDate
from pydantic_extra_types.phone_numbers import PhoneNumber
from sqlalchemy import (
	Boolean,
	CheckConstraint,
	Date,
	Enum,
	String,
	text,
)
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums.gender import Gender
from app.models.base_class import Base

if TYPE_CHECKING:
	from app.models.structured.order import Order


class User(Base):
	"""User model class representing the 'users' table"""

	__tablename__ = "users"

	id: Mapped[UUID4] = mapped_column(
		UUID(),
		nullable=False,
		primary_key=True,
		index=True,
		unique=True,
		server_default=text("(gen_random_uuid())"),
		comment="ID of the User",
	)
	username: Mapped[str] = mapped_column(
		String(15),
		nullable=False,
		index=True,
		unique=True,
		comment="Unique username used for login and identification",
	)
	email: Mapped[EmailStr] = mapped_column(
		String(320),
		nullable=False,
		index=True,
		unique=True,
		comment="User's email address, used for contact and authentication",
	)
	first_name: Mapped[str] = mapped_column(
		String(50),
		nullable=False,
		comment="User's first name(s)",
	)
	last_name: Mapped[str] = mapped_column(
		String(100),
		nullable=False,
		comment="User's last name(s)",
	)
	password: Mapped[str] = mapped_column(
		String(60),
		nullable=False,
		comment="User's password (hashed)",
	)
	gender: Mapped[Gender] = mapped_column(
		Enum(Gender),
		nullable=True,
		comment="User's gender (optional)",
	)
	birthdate: Mapped[PastDate] = mapped_column(
		Date,
		nullable=True,
		comment="User's date of birth (optional)",
	)
	phone_number: Mapped[PhoneNumber] = mapped_column(
		String(20),
		nullable=True,
		comment="User's contact phone number (optional)",
	)
	is_active: Mapped[bool] = mapped_column(
		Boolean(),
		default=True,
		nullable=False,
		server_default=text("true"),
		comment="Indicates whether the user account is active",
	)
	is_superuser: Mapped[bool] = mapped_column(
		Boolean(),
		default=False,
		nullable=False,
		server_default=text("false"),
		comment="True if the user has superuser privileges",
	)
	created_at: Mapped[datetime] = mapped_column(
		TIMESTAMP(timezone=True),
		default=datetime.now,
		server_default=text("now()"),
		comment="Timestamp when the user was created",
	)
	updated_at: Mapped[datetime] = mapped_column(
		TIMESTAMP(timezone=True),
		nullable=True,
		comment="Timestamp when the user was last updated",
	)

	orders: Mapped[list["Order"]] = relationship("Order", back_populates="user")

	__table_args__ = (
		CheckConstraint(
			"char_length(username) >= 4", name="users_username_length"
		),
		CheckConstraint("char_length(email) >= 3", name="users_email_length"),
		CheckConstraint(
			"char_length(password) = 60", name="users_password_length"
		),
		CheckConstraint(
			"email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}$'",
			name="users_email_format",
		),
		CheckConstraint(
			"char_length(first_name) >= 1", name="users_first_name_length"
		),
		CheckConstraint(
			"char_length(last_name) >= 1", name="users_last_name_length"
		),
		CheckConstraint(
			"phone_number ~ '^tel:\\+\\d{3}-\\d{2}-\\d{3}-\\d{4}$'",
			name="users_phone_number_format",
		),
	)
