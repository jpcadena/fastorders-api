from typing import Annotated

import uvicorn
from fastapi import Depends, FastAPI, status
from fastapi.responses import ORJSONResponse, RedirectResponse
from pydantic import PositiveInt
from sqlalchemy.ext.asyncio import AsyncSession

# from app.api.api_v1.api import api_router
# from app.core.lifecycle import lifespan
from app.db.session import check_db_health, get_session

app: FastAPI = FastAPI(
	debug=True,
	default_response_class=ORJSONResponse,
	# lifespan=lifespan,
)
# app.include_router(api_router, prefix="/api/v1")


@app.get(
	"/",
	status_code=status.HTTP_307_TEMPORARY_REDIRECT,
	response_class=RedirectResponse,
)
async def redirect_to_docs() -> RedirectResponse:
	"""
	**Redirects the user to the /docs endpoint for API documentation.**

	## Returns:
		RedirectResponse: The redirect response.
	"""
	return RedirectResponse("/docs")


@app.get(
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


if __name__ == "__main__":
	uvicorn.run(
		"main:app",
		host="",
		port=8081,
		reload=True,
		log_level="info",
	)
