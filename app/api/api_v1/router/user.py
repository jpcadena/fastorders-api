"""
A module for user in the app.api.api_v1.router package.
"""

import logging
from typing import Annotated
from uuid import uuid4

from fastapi import APIRouter, Body, Depends, HTTPException, Path, status
from fastapi.responses import ORJSONResponse
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.models.structured import User
from app.repositories.structured.user_repository import UserRepository
from app.schemas.user import UserCreate, UserResponse, UserUpdate

logger: logging.Logger = logging.getLogger(__name__)
router: APIRouter = APIRouter(prefix="/user", tags=["user"])


@router.get("/{user_id}", response_model=UserResponse)
async def get_use_by_id(
	user_id: Annotated[
		UUID4,
		Path(
			...,
			title="User ID",
			description="ID of the user to retrieve.",
			example=uuid4(),
		),
	],
	db: AsyncSession = Depends(get_session),
) -> UserResponse:
	"""
	**Get a user by ID from the database.**

	## Args:
		user_id (UUID4): The user ID

	## Returns:
		UserResponse: The user data if found
	"""
	user_repository: UserRepository = UserRepository(session=db)
	user: User | None = await user_repository.get(user_id)
	if not user:
		msg: str = (
			f"The user with id: {user_id} has not been found on the system"
		)
		logger.error(msg)
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=msg)
	return UserResponse.model_validate(user)


@router.get("", response_model=list[UserResponse])
async def get_all_users(
	db: AsyncSession = Depends(get_session),
):
	"""
	**Retrieve all users from the system.**

	## Returns:
		List[UserResponse]: A list of all registered users
	"""
	user_repository: UserRepository = UserRepository(session=db)
	users: list[User] = await user_repository.get_all()
	return [UserResponse.model_validate(user) for user in users]


@router.post(
	"", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def create_user(
	user_create: Annotated[
		UserCreate,
		Body(
			...,
			title="User create",
			description="User data to create",
		),
	],
	db: AsyncSession = Depends(get_session),
):
	"""
	**Create a new user in the database.**

	## Args:
		user_create (UserCreate): User creation schema

	## Returns:
		UserResponse: Created user object
	"""
	user_repository: UserRepository = UserRepository(session=db)
	user: User = User(**user_create.model_dump())
	new_user: User = await user_repository.create(user)
	return UserResponse.model_validate(new_user)


@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(
	user_id: Annotated[
		UUID4,
		Path(
			title="User ID",
			description="ID of the user to update",
			example=uuid4(),
		),
	],
	user_update: Annotated[
		UserUpdate,
		Body(
			...,
			title="User update",
			description="User data to update",
		),
	],
	db: AsyncSession = Depends(get_session),
):
	"""
	**Update user fields by ID.**

	## Args:
		user_id (UUID4): The user ID
		user_update (UserUpdate): Fields to update

	## Returns:
		UserResponse: Updated user
	"""
	user_repository: UserRepository = UserRepository(session=db)
	user: User | None = await user_repository.get(user_id)
	if not user:
		msg: str = "User not found"
		logger.error(msg)
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=msg)
	updated_user: User = await user_repository.update(
		user, user_update.model_dump(exclude_unset=True)
	)
	return UserResponse.model_validate(updated_user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
	user_id: Annotated[UUID4, Path(title="User ID")],
	db: AsyncSession = Depends(get_session),
):
	"""
	**Delete a user by ID.**

	## Args:
		user_id (UUID4): The user ID

	## Returns:
		ORJSONResponse: An object containing the flag if the user was deleted or not
	"""
	user_repository: UserRepository = UserRepository(session=db)
	success: bool = await user_repository.delete(user_id)
	if not success:
		msg: str = "User not found"
		logger.error(msg)
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=msg)
	return ORJSONResponse(
		status_code=status.HTTP_204_NO_CONTENT, content={"deleted": success}
	)
