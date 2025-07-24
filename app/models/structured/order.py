"""
A module for order in the app.models package.
"""

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import UUID4
from sqlalchemy import Float, ForeignKey, text
from sqlalchemy.dialects.postgresql import JSONB, TIMESTAMP, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_class import Base

if TYPE_CHECKING:
	from app.models.structured.user import User


class Order(Base):
	"""Order model class representing the 'orders' table"""

	__tablename__ = "orders"

	id: Mapped[UUID4] = mapped_column(
		UUID(),
		nullable=False,
		primary_key=True,
		index=True,
		unique=True,
		server_default=text("(gen_random_uuid())"),
		comment="ID of the Order",
	)
	user_id: Mapped[UUID4] = mapped_column(
		UUID(as_uuid=True),
		ForeignKey("users.id", ondelete="CASCADE"),
		nullable=False,
		comment="Foreign key referencing the ID of the User who placed the order",
	)
	total_amount: Mapped[float] = mapped_column(
		Float,
		nullable=False,
		comment="Total cost of all products in the order",
	)
	items: Mapped[list] = mapped_column(
		JSONB,
		nullable=False,
		comment="List of product items in JSON format (id, quantity, price)",
	)
	created_at: Mapped[datetime] = mapped_column(
		TIMESTAMP(timezone=True),
		default=datetime.now,
		server_default=text("now()"),
		comment="Timestamp when the order was placed",
	)

	user: Mapped["User"] = relationship("User", back_populates="orders")
