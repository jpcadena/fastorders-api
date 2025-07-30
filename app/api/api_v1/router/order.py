"""
A module for order in the app.api.api_v1.router package.
"""

import logging
from typing import Annotated
from uuid import uuid4

from fastapi import APIRouter, Body, Depends, HTTPException, Path, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.models.structured import Order
from app.repositories.structured.order_repository import OrderRepository
from app.schemas.order import OrderCreate, OrderResponse

logger: logging.Logger = logging.getLogger(__name__)
router: APIRouter = APIRouter(prefix="/order", tags=["order"])


@router.get("", response_model=list[OrderResponse])
async def get_all_orders(
	db: AsyncSession = Depends(get_session),
) -> list[OrderResponse]:
	"""
	**Retrieve all orders.**

	## Returns:
		List[OrderResponse]: A list of orders including order items
	"""
	order_repository: OrderRepository = OrderRepository(session=db)
	orders: list[Order] = await order_repository.get_all()
	return [OrderResponse.model_validate(order) for order in orders]


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order_by_id(
	order_id: Annotated[
		UUID4,
		Path(
			...,
			title="Order ID",
			description="UUID of the order to retrieve",
			example=uuid4(),
		),
	],
	db: AsyncSession = Depends(get_session),
) -> OrderResponse:
	"""
	**Get an order by its UUID.**

	## Args:
		order_id (UUID4): Order ID

	## Returns:
		OrderResponse: The found order including its items
	"""
	order_repository: OrderRepository = OrderRepository(session=db)
	order: Order | None = await order_repository.get(order_id)
	if not order:
		msg: str = f"Order with ID {order_id} not found"
		logger.error(msg)
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=msg)
	return OrderResponse.model_validate(order)


@router.post(
	"",
	response_model=OrderResponse,
	status_code=status.HTTP_201_CREATED,
)
async def create_order(
	order_create: Annotated[
		OrderCreate,
		Body(
			...,
			title="Order create",
			description="Order data with related order items",
		),
	],
	db: AsyncSession = Depends(get_session),
):
	"""
	**Create a new order with associated order items.**

	## Args:
		order_create (OrderCreate): Data for the new order

	## Returns:
		OrderResponse: The created order with nested items
	"""
	order_repository: OrderRepository = OrderRepository(session=db)
	order: Order = await order_repository.create_with_items(order_create)
	return OrderResponse.model_validate(order)
