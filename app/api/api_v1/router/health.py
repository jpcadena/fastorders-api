"""
A module for health in the app.api.api v1.router package.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.responses import ORJSONResponse
from pydantic import PositiveInt
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import check_db_health, get_session

router: APIRouter = APIRouter(prefix="/order", tags=["order"])


@router.get(
	"/health",
)
async def check_health(
	session: Annotated[AsyncSession, Depends(get_session)],
) -> ORJSONResponse:
	"""
	**Check the health of the application backend.**

	## Returns:
		ORJSONResponse: The JSON response from the health check

	\f
	Args:
		session (AsyncSession): The database session as a dependency injection
	"""
	health_status: dict[str, str] = {
		"status": "healthy",
	}
	status_code: PositiveInt = status.HTTP_200_OK
	if not await check_db_health(session):
		health_status["status"] = "unhealthy"
		status_code = status.HTTP_503_SERVICE_UNAVAILABLE
	return ORJSONResponse(health_status, status_code=status_code)
