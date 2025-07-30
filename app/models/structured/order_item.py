"""
A module for order item in the app.models.structured package.
"""

from typing import TYPE_CHECKING

from pydantic import UUID4, NonNegativeFloat, PositiveInt
from sqlalchemy import CheckConstraint, Float, ForeignKey, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.sqltypes import Integer

from app.models.base_class import Base

if TYPE_CHECKING:
	from app.models.structured.order import Order
	from app.models.structured.product import Product


class OrderItem(Base):
	__tablename__ = "order_items"

	id: Mapped[UUID4] = mapped_column(
		UUID(),
		nullable=False,
		primary_key=True,
		index=True,
		unique=True,
		server_default=text("(gen_random_uuid())"),
		comment="ID of the Order Item",
	)
	order_id: Mapped[UUID4] = mapped_column(
		UUID(),
		ForeignKey("orders.id", ondelete="CASCADE"),
		nullable=False,
		comment="Foreign key to the related order",
	)
	product_id: Mapped[UUID4] = mapped_column(
		UUID(),
		ForeignKey("products.id", ondelete="CASCADE"),
		nullable=False,
		comment="Foreign key to the ordered product",
	)
	quantity: Mapped[PositiveInt] = mapped_column(
		Integer,
		nullable=False,
		comment="Number of product units in the order item",
	)
	price_at_purchase: Mapped[NonNegativeFloat] = mapped_column(
		Float,
		nullable=False,
		comment="Unit price of the product at the time of the order",
	)

	order: Mapped["Order"] = relationship("Order", back_populates="order_items")
	product: Mapped["Product"] = relationship(
		"Product", back_populates="order_items"
	)

	__table_args__ = (
		CheckConstraint("quantity > 0", name="order_item_quantity_positive"),
		CheckConstraint(
			"price_at_purchase >= 0",
			name="order_item_price_at_purchase_positive",
		),
	)
