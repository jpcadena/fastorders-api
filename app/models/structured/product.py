"""
A module for product in the app.models package.
"""

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import UUID4, NonNegativeFloat, NonNegativeInt
from sqlalchemy import Boolean, CheckConstraint, Float, String, Text, text
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.sqltypes import Integer

from app.models.base_class import Base

if TYPE_CHECKING:
	from app.models.structured.order_item import OrderItem


class Product(Base):
	"""Product model class representing the 'products' table"""

	__tablename__ = "products"

	id: Mapped[UUID4] = mapped_column(
		UUID(),
		nullable=False,
		primary_key=True,
		index=True,
		unique=True,
		server_default=text("(gen_random_uuid())"),
		comment="ID of the Product",
	)
	name: Mapped[str] = mapped_column(
		String(100),
		nullable=False,
		index=True,
		comment="Name of the product",
	)
	description: Mapped[str] = mapped_column(
		Text,
		nullable=True,
		comment="Detailed description of the product",
	)
	price: Mapped[NonNegativeFloat] = mapped_column(
		Float,
		nullable=False,
		comment="Selling price of the product",
	)
	stock: Mapped[NonNegativeInt] = mapped_column(
		Integer,
		nullable=False,
		server_default=text("0"),
		comment="Available stock units of the product",
	)
	category: Mapped[str] = mapped_column(
		String(50),
		nullable=True,
		comment="Optional category label for grouping similar products",
	)
	is_active: Mapped[bool] = mapped_column(
		Boolean,
		default=True,
		nullable=False,
		server_default=text("true"),
		comment="True if the product is visible and active in the store",
	)
	created_at: Mapped[datetime] = mapped_column(
		TIMESTAMP(timezone=True),
		default=datetime.now,
		server_default=text("now()"),
		comment="Timestamp when the product was created",
	)
	updated_at: Mapped[datetime] = mapped_column(
		TIMESTAMP(timezone=True),
		nullable=True,
		comment="Timestamp of the last update to the product details",
	)
	order_items: Mapped[list["OrderItem"]] = relationship(
		"OrderItem", back_populates="product"
	)

	__table_args__ = (
		CheckConstraint("price >= 0", name="products_price_positive"),
		CheckConstraint("stock >= 0", name="products_stock_positive"),
	)
