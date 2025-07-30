"""
A module for order items in the app.api.api_v1.router package.
"""

import logging
from typing import Annotated
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Path, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.models.structured import OrderItem
from app.repositories.structured.order_item_repository import (
	OrderItemRepository,
)
from app.schemas.order_item import OrderItemResponse

logger: logging.Logger = logging.getLogger(__name__)
router: APIRouter = APIRouter(prefix="/order-item", tags=["order-item"])


@router.get("/{item_id}", response_model=OrderItemResponse)
async def get_order_item_by_id(
	item_id: Annotated[
		UUID4,
		Path(
			...,
			title="Order Item ID",
			description="ID of the order item to retrieve",
			example=uuid4(),
		),
	],
	db: AsyncSession = Depends(get_session),
) -> OrderItemResponse:
	"""
	**Retrieve an order item by its ID.**

	## Args:
		item_id (UUID4): OrderItem UUID

	## Returns:
		OrderItemResponse: The order item data
	"""
	order_item_repository: OrderItemRepository = OrderItemRepository(session=db)
	item: OrderItem | None = await order_item_repository.get(item_id)
	if not item:
		msg: str = f"OrderItem with ID {item_id} not found"
		logger.exception(msg)
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=msg)
	return OrderItemResponse.model_validate(item)


@router.get("/", response_model=list[OrderItemResponse])
async def list_all_order_items(
	db: AsyncSession = Depends(get_session),
) -> list[OrderItemResponse]:
	"""
	**List all order items.**

	## Returns:
		List[OrderItemResponse]: All order items in the database
	"""
	order_item_repository: OrderItemRepository = OrderItemRepository(session=db)
	items: list[OrderItem] = await order_item_repository.get_all()
	return [OrderItemResponse.model_validate(item) for item in items]
