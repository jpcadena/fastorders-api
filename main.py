import base64
from functools import partial
from typing import Annotated

import uvicorn
from fastapi import Depends, FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, ORJSONResponse, RedirectResponse
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
from app.utils.openapi_utils import custom_generate_unique_id, custom_openapi

app: FastAPI = FastAPI(
	openapi_url=f"{auth_setting.API_V1_STR}{init_setting.OPENAPI_FILE_PATH}",
	debug=True,
	default_response_class=ORJSONResponse,
	lifespan=lifespan,
	generate_unique_id_function=custom_generate_unique_id,
	docs_url=None,
)
app.openapi = partial(custom_openapi, app)
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_methods=["*"],
	allow_headers=["*"],
	allow_credentials=True,
)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(GZipMiddleware)

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
	include_in_schema=False,
)
async def redirect_to_docs() -> RedirectResponse:
	"""
	**Redirects the user to the /docs endpoint for API documentation.**

	## Returns:
		RedirectResponse: The redirect response.
	"""
	return RedirectResponse("/docs")


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html(request: Request) -> HTMLResponse:
	"""
	Custom Swagger UI for API documentation page in HTML

	Args:
		request (Request): The FastAPI request from the server

	Returns:
		HTMLResponse: The response in HTML
	"""
	root_path = request.scope.get("root_path", "").rstrip("/")
	openapi_url = root_path + app.openapi_url
	oauth2_redirect_url = app.swagger_ui_oauth2_redirect_url
	if oauth2_redirect_url:
		oauth2_redirect_url = root_path + oauth2_redirect_url
	js_code: str = f"""
	    const ui = SwaggerUIBundle({{
	        url: '{openapi_url}',
	        dom_id: '#swagger-ui',
	        layout: 'BaseLayout',
	        deepLinking: true,
	        showExtensions: true,
	        showCommonExtensions: true,
	        oauth2RedirectUrl: '{oauth2_redirect_url}',
	        presets: [
	            SwaggerUIBundle.presets.apis,
	            SwaggerUIBundle.SwaggerUIStandalonePreset
	        ]
	    }});
	    """  # noqa: E101
	js_base64: str = base64.b64encode(js_code.encode("utf-8")).decode("utf-8")
	return HTMLResponse(f"""
	    <!DOCTYPE html>
	    <html>
	    <head>
	        <link type="text/css" rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css">
	        <link rel="shortcut icon" href="https://fastapi.tiangolo.com/img/favicon.png">
	        <title>FastAPI - Swagger UI</title>
	    </head>
	    <body>
	        <div id="swagger-ui"></div>
	        <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
	        <script src="data:text/javascript;base64,{js_base64}"></script>
	    </body>
	    </html>
	    """)  # noqa: E101


@app.get("/health")
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
	print("ok")
	print(session)
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
