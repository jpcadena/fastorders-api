"""
A module for order in the app.schemas package.
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, NonNegativeFloat


class OrderBase(BaseModel):
	"""Base schema for order shared across operations."""

	user_id: UUID = Field(..., description="User ID")
	total_amount: NonNegativeFloat = Field(..., description="Total amount")


class OrderCreate(OrderBase):
	"""Schema for creating a new order."""

	model_config = ConfigDict(from_attributes=True)


class OrderUpdate(BaseModel):
	"""Schema for updating an order."""

	total_amount: NonNegativeFloat | None = Field(
		None, description="Total amount"
	)


class OrderResponse(OrderBase):
	"""Response schema for an order."""

	model_config = ConfigDict(from_attributes=True)

	id: UUID = Field(..., description="Order ID")
	created_at: datetime = Field(..., description="Order creation datetime")
