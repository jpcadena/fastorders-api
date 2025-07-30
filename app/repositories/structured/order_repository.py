"""
Provides CRUD operations for the Order model.
"""

from uuid import UUID

from fastapi import HTTPException, status
from pydantic import UUID4, NonNegativeFloat
from sqlalchemy import Result, Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.structured import Order, OrderItem, Product
from app.repositories.base_sql_repository import BaseRepository
from app.schemas.order import OrderCreate


class OrderRepository(BaseRepository[Order]):
	"""Repository for performing CRUD operations on Order model."""

	def __init__(self, session: AsyncSession):
		"""
		Initialize the OrderRepository with an async session.

		Args:
			session (AsyncSession): The database session.
		"""
		super().__init__(Order, session)

	async def get(self, _id: UUID4) -> Order | None:
		"""
		Retrieve an Order by their UUID4.

		Args:
			_id (UUID4): The Order's UUID.

		Returns:
			Order | None: The Order instance or None if not found.
		"""
		return await super().get(_id)

	async def delete(self, _id: UUID4) -> bool:
		"""
		Delete an Order by their UUID4.

		Args:
			_id (UUID4): The Order's UUID.

		Returns:
			bool: True if deletion was successful, False otherwise.
		"""
		return await super().delete(_id)

	async def get_by_user_id(self, user_id: UUID4) -> list[Order]:
		"""
		Retrieve all orders made by a specific user.

		Args:
			user_id (UUID4): The ID of the user.

		Returns:
			list[Order]: A list of orders placed by the user.
		"""
		stmt: Select = select(self.model).where(self.model.user_id == user_id)
		result: Result = await self.session.execute(stmt)
		return list(result.scalars().all())

	async def create_with_items(self, order: OrderCreate) -> Order:
		"""
		Create an order with items

		Args:
			order (OrderCreate): The order to create.

		Returns:
			Order: The created Order object

		Raises:
			HTTPException: If no product is found or if they are inactive.
		"""
		user_id: UUID = order.user_id
		items: list[OrderItem] = []
		total_amount: NonNegativeFloat = 0.0
		for item in order.order_items:
			product: Product | None = await self.session.get(
				Product, item.product_id
			)
			if not product or not product.is_active:
				raise HTTPException(
					status_code=status.HTTP_404_NOT_FOUND,
					detail=f"Invalid product ID: {item.product_id}",
				)
			price: NonNegativeFloat = product.price
			total_amount += price * item.quantity
			items.append(
				OrderItem(
					product_id=item.product_id,
					quantity=item.quantity,
					price_at_purchase=price,
				)
			)
		order: Order = Order(
			user_id=user_id,
			total_amount=total_amount,
			order_items=items,
		)
		self.session.add(order)
		await self.session.flush()
		return order
