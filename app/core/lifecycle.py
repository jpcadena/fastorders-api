"""
A module for lifecycle in the app.core package.
"""

import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI

from app.config.config import get_auth_settings, get_init_settings, get_settings
from app.db.init_db import init_db

logger: logging.Logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(application: FastAPI) -> AsyncGenerator[Any]:  # noqa: ARG001
	"""
	Handles the lifecycle of the FastAPI application.

	Args:
		application (FastAPI): The FastAPI application

	Returns:
		AsyncGenerator[Any]: An async generator yielding the lifecycle.
	"""
	logger.info("Starting API...")
	try:
		application.state.settings = get_settings()
		application.state.init_settings = get_init_settings()
		application.state.auth_settings = get_auth_settings()
		logger.info("Configuration settings loaded.")
		await init_db()
		logger.info("Database initialized.")
		yield
	except Exception as exc:
		logger.error(f"Error during application startup: {exc}")
		raise
	finally:
		logger.info("Application shutdown completed.")
