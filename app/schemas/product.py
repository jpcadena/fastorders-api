"""
A module for product in the app.schemas package.
"""

from datetime import datetime
from uuid import UUID

from pydantic import (
	BaseModel,
	ConfigDict,
	Field,
	NonNegativeFloat,
	NonNegativeInt,
)


class ProductBase(BaseModel):
	"""Base schema for product shared across operations."""

	name: str = Field(..., title="Product name", max_length=100)
	description: str | None = Field(None, title="Product description")
	price: NonNegativeFloat = Field(..., title="Price")
	stock: NonNegativeInt | NonNegativeFloat = Field(..., title="Stock units")
	category: str | None = Field(None, title="Category", max_length=50)
	is_active: bool = Field(default=True, title="Product status")


class ProductCreate(ProductBase):
	"""Schema for creating a new product."""

	model_config = ConfigDict(from_attributes=True)


class ProductUpdate(BaseModel):
	"""Schema for updating a product."""

	name: str | None = Field(None, title="Product name", max_length=100)
	description: str | None = Field(None, title="Product description")
	price: NonNegativeFloat | None = Field(None, title="Price")
	stock: NonNegativeInt | None = Field(None, title="Stock units")
	category: str | None = Field(None, title="Category", max_length=50)
	is_active: bool | None = Field(None, title="Product status")


class ProductResponse(ProductBase):
	"""Response schema for a product."""

	model_config = ConfigDict(from_attributes=True)

	id: UUID = Field(..., title="Product ID")
	created_at: datetime = Field(..., title="Creation datetime")
	updated_at: datetime | None = Field(None, title="Last update datetime")
