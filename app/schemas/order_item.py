"""
A module for order item in the app.schemas package.
"""

from pydantic import (
	UUID4,
	BaseModel,
	ConfigDict,
	Field,
	NonNegativeFloat,
	PositiveInt,
)


class OrderItemBase(BaseModel):
	"""Base schema for order item shared across operations."""

	product_id: UUID4 = Field(..., description="Product ID")
	quantity: PositiveInt = Field(..., description="Quantity")
	price_at_purchase: NonNegativeFloat = Field(
		..., description="Price at purchase"
	)


class OrderItemCreate(OrderItemBase):
	"""Schema for creating a new order item."""

	model_config = ConfigDict(from_attributes=True)


class OrderItemUpdate(BaseModel):
	"""Schema for updating an order item."""

	quantity: PositiveInt | None = Field(None, description="Quantity")
	price_at_purchase: NonNegativeFloat | None = Field(
		None, description="Price at purchase"
	)


class OrderItemResponse(OrderItemBase):
	"""Response schema for an order item."""

	model_config = ConfigDict(from_attributes=True)

	id: UUID4 = Field(..., description="Order Item ID")
	order_id: UUID4 = Field(..., description="Related Order ID")
