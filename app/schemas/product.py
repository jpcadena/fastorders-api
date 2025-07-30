"""
A module for product in the app.schemas package.
"""

from datetime import datetime

from pydantic import (
	UUID4,
	BaseModel,
	ConfigDict,
	Field,
	NonNegativeFloat,
	NonNegativeInt,
)


class ProductBase(BaseModel):
	"""Base schema for product shared across operations."""

	name: str = Field(..., description="Product name", max_length=100)
	description: str | None = Field(None, description="Product description")
	price: NonNegativeFloat = Field(..., description="Product price")
	stock: NonNegativeInt | NonNegativeFloat = Field(
		..., description="Stock units"
	)
	category: str | None = Field(
		None, description="Category of the product", max_length=50
	)
	is_active: bool = Field(default=True, description="Product status")


class ProductCreate(ProductBase):
	"""Schema for creating a new product."""

	model_config = ConfigDict(from_attributes=True)


class ProductUpdate(BaseModel):
	"""Schema for updating a product."""

	name: str | None = Field(None, description="Product name", max_length=100)
	description: str | None = Field(None, description="Product description")
	price: NonNegativeFloat | None = Field(None, description="Product price")
	stock: NonNegativeInt | None = Field(None, description="Stock units")
	category: str | None = Field(
		None, description="Category of the product", max_length=50
	)
	is_active: bool | None = Field(None, description="Product status")


class ProductResponse(ProductBase):
	"""Response schema for a product."""

	model_config = ConfigDict(from_attributes=True)

	id: UUID4 = Field(..., description="Product ID")
	created_at: datetime = Field(..., description="Creation datetime")
	updated_at: datetime | None = Field(
		None, description="Last update datetime"
	)
