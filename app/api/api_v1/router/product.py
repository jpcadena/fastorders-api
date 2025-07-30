"""
A module for product in the app.api.api_v1.router package.
"""

import logging
from typing import Annotated
from uuid import uuid4

from fastapi import APIRouter, Body, Depends, HTTPException, Path, status
from fastapi.responses import ORJSONResponse
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.models.structured import Product
from app.repositories.structured.product_repository import ProductRepository
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate

logger: logging.Logger = logging.getLogger(__name__)
router: APIRouter = APIRouter(prefix="/product", tags=["product"])


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
	product_id: Annotated[
		UUID4,
		Path(
			...,
			title="Product ID",
			description="ID of the product to retrieve",
			example=uuid4(),
		),
	],
	db: AsyncSession = Depends(get_session),
) -> ProductResponse:
	"""
	**Get a product by ID.**

	## Args:
		product_id (UUID4): UUID of the product

	## Returns:
		ProductResponse: The found product
	"""
	product_repository: ProductRepository = ProductRepository(session=db)
	product: Product | None = await product_repository.get(product_id)
	if not product:
		msg: str = f"The product with id: {product_id} has not been found on the system"
		logger.error(msg)
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=msg)
	return ProductResponse.model_validate(product)


@router.get("/name/{name}", response_model=ProductResponse)
async def get_product_by_name(
	name: Annotated[
		str,
		Path(
			...,
			title="Product Name",
			description="Name of the product",
			example="product-name",
		),
	],
	db: AsyncSession = Depends(get_session),
) -> ProductResponse:
	"""
	**Get a product by its name.**

	## Args:
		name (str): Name of the product

	## Returns:
		ProductResponse: The found product
	"""
	product_repository: ProductRepository = ProductRepository(session=db)
	product: Product | None = await product_repository.get_by_name(name)
	if not product:
		msg: str = f"Product {name} not found"
		logger.error(msg)
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=msg)
	return ProductResponse.model_validate(product)


@router.post(
	"", response_model=ProductResponse, status_code=status.HTTP_201_CREATED
)
async def create_product(
	product_create: Annotated[
		ProductCreate,
		Body(
			...,
			title="Product create",
			description="Product data to create",
		),
	],
	db: AsyncSession = Depends(get_session),
) -> ProductResponse:
	"""
	**Create a new product.**

	## Args:
		product_create (ProductCreate): Schema with product data

	## Returns:
		ProductResponse: Created product
	"""
	product_repository: ProductRepository = ProductRepository(session=db)
	product: Product = Product(**product_create.model_dump())
	new_product: Product = await product_repository.create(product)
	return ProductResponse.model_validate(new_product)


@router.patch("/{product_id}", response_model=ProductResponse)
async def update_product(
	product_id: Annotated[
		UUID4,
		Path(
			...,
			title="Product ID",
			description="ID of the product to update",
			example=uuid4(),
		),
	],
	product_in: Annotated[
		ProductUpdate,
		Body(
			...,
			title="Product update",
			description="Product data to update",
		),
	],
	db: AsyncSession = Depends(get_session),
) -> ProductResponse:
	"""
	**Update fields of an existing product.**

	## Args:
		product_id (UUID4): ID of the product
		product_in (ProductUpdate): Updated fields

	## Returns:
		ProductResponse: Updated product
	"""
	product_repository: ProductRepository = ProductRepository(session=db)
	product: Product | None = await product_repository.get(product_id)
	if not product:
		msg: str = f"Product with ID {product_id} not found"
		logger.error(msg)
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=msg)
	updated_product: Product = await product_repository.update(
		product, product_in.model_dump(exclude_unset=True)
	)
	return ProductResponse.model_validate(updated_product)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def soft_delete_product(
	product_id: Annotated[
		UUID4,
		Path(
			...,
			title="Product ID",
			description="Product ID to deactivate",
			example=uuid4(),
		),
	],
	db: AsyncSession = Depends(get_session),
):
	"""
	**Soft delete a product (set is_active = False).**

	## Args:
		product_id (UUID4): Product to deactivate

	## Returns:
		ORJSONResponse: An object containing the flag if the product was deleted or not
	"""
	product_repository: ProductRepository = ProductRepository(session=db)
	success: bool = await product_repository.soft_delete(product_id)
	if not success:
		msg: str = f"Product with ID {product_id} not found"
		logger.error(msg)
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=msg)
	return ORJSONResponse(
		status_code=status.HTTP_204_NO_CONTENT, content={"deleted": success}
	)
