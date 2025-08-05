"""
A module for openapi utils in the app.utils package.
"""

import json
from typing import Any

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.routing import APIRoute


def remove_tag_from_operation_id(tag: str, operation_id: str) -> str:
	"""
	Removes a specific tag prefix from the given operation ID.

	Args:
		tag (str): The tag to remove from the operation ID.
		operation_id (str): The original operation ID.

	Returns:
		str: The updated operation ID without the tag prefix.
	"""
	return operation_id.removeprefix(f"{tag}-")


def update_operation_id(operation: dict[str, Any]) -> None:
	"""
	Updates the operationId of an OpenAPI operation by removing the tag prefix.

	Args:
		operation (dict[str, Any]): The OpenAPI operation object.

	Returns:
		NoneType: None
	"""
	if operation.get(
		"tags",
	):
		tag: str = operation["tags"][0]
		operation_id: str = operation["operationId"]
		new_operation_id: str = remove_tag_from_operation_id(tag, operation_id)
		operation["operationId"] = new_operation_id


def modify_json_data(
	data: dict[str, dict[str, Any]],
) -> dict[str, dict[str, Any]]:
	"""
	Modifies the OpenAPI JSON data by updating operationIds in the paths.

	Args:
		data (dict[str, dict[str, Any]]): The OpenAPI JSON schema to modify.

	Returns:
		dict[str, dict[str, Any]]: The modified OpenAPI schema.
	"""
	paths: dict[str, dict[str, dict[str, Any]]] | None = data.get("paths")
	if not paths:
		return data
	for key, path_data in paths.items():
		if key == "/":
			continue
		for operation in dict(path_data).values():
			update_operation_id(operation)
	return data


def custom_generate_unique_id(route: APIRoute) -> str:
	"""
	Generates a custom unique ID for API routes based on tags and route names.

	Args:
		route (APIRoute): The FastAPI route object.

	Returns:
		str: A unique ID composed of the route's tag and name.
	"""
	if route.name in (
		"redirect_to_docs",
		"custom_swagger_ui_html",
		"check_health",
	):
		return str(route.name)
	return f"{route.tags[0]}-{route.name}"


def write_schema_to_file(
	schema: dict[str, dict[str, Any]], file_path: str, encoding: str
) -> None:
	"""
	Writes the given OpenAPI schema to a file in JSON format.

	Args:
		schema (dict[str, dict[str, Any]]): The OpenAPI schema to write.
		file_path (str): The file path where the schema should be saved.
		encoding (str): The file encoding to use.

	Returns:
		NoneType: None
	"""
	with open(file_path, mode="w", encoding=encoding) as out_file:
		out_file.write(json.dumps(schema, indent=4))


def custom_openapi(app: FastAPI) -> dict[str, Any]:
	"""
	Generates and caches a custom OpenAPI schema for the FastAPI application.

	This function uses FastAPI's default OpenAPI generation, applies custom
	modifications, and writes the schema to a file. The schema is cached for
	future use to avoid regeneration on every request.

	Args:
		app (FastAPI): The FastAPI application instance.

	Returns:
		dict[str, Any]: The customized OpenAPI schema.
	"""
	if app.openapi_schema:
		return app.openapi_schema
	openapi_schema: dict[str, dict[str, Any]] = get_openapi(
		title=app.state.init_settings.API_NAME,
		version=app.state.init_settings.VERSION,
		summary=app.state.init_settings.SUMMARY,
		description=app.state.init_settings.DESCRIPTION,
		routes=app.routes,
		servers=[
			{
				"url": app.state.auth_settings.SERVER_URL,
				"description": app.state.auth_settings.SERVER_DESCRIPTION,
			}
		],
		contact=app.state.settings.CONTACT,
		license_info=app.state.init_settings.LICENSE_INFO,
	)
	openapi_schema = modify_json_data(openapi_schema)
	app.openapi_schema = openapi_schema
	write_schema_to_file(
		openapi_schema,
		f"{app.state.init_settings.OPENAPI_FILE_PATH}"[1:],
		app.state.init_settings.ENCODING,
	)
	return app.openapi_schema
