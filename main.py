from typing import Annotated

import uvicorn
from fastapi import Depends, FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import ORJSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import PositiveInt
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.api_v1.api import api_router
from app.config.config import auth_setting, init_setting, setting
from app.core.lifecycle import lifespan
from app.db.session import check_db_health, get_session
from app.middlewares.security_headers_middleware import (
	SecurityHeadersMiddleware,
)

app: FastAPI = FastAPI(
	debug=True,
	default_response_class=ORJSONResponse,
	lifespan=lifespan,
)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(GZipMiddleware)
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_methods=["*"],
	allow_headers=["*"],
	allow_credentials=True,
)
app.mount(
	init_setting.ASSETS_DIR,
	StaticFiles(
		directory=init_setting.ASSETS_APP,
	),
	name=init_setting.ASSETS_APP,
)
templates: Jinja2Templates = Jinja2Templates(
	directory=init_setting.TEMPLATES_DIR, autoescape=False, auto_reload=True
)
app.include_router(api_router, prefix=auth_setting.API_V1_STR)


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
		host=f"{setting.HOST}",
		port=setting.PORT,
		reload=setting.SERVER_RELOAD,
		log_level=setting.SERVER_LOG_LEVEL,
	)
