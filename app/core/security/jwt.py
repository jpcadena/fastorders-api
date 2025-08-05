"""
This module handles JSON Web Token (JWT) creation for authentication
 and authorization.
"""

import logging
from datetime import UTC, datetime, timedelta
from typing import Annotated, Any

from authlib.jose import JoseError, jwt
from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from pydantic import NonNegativeFloat

from app.config.auth_settings import AuthSettings
from app.config.config import get_auth_settings
from app.core.enums.toke_type import TokenType
from app.schemas.external.token_payload import TokenPayload

logger: logging.Logger = logging.getLogger(__name__)


def _generate_expiration_time(
	expires_delta: timedelta | None,
	minutes: NonNegativeFloat | None = None,
) -> datetime:
	"""
	Generate an expiration time for JWT

	Args:
		expires_delta (timedelta | None): The timedelta specifying when the
		token should expire
		minutes (NonNegativeFloat | None): The minutes to add to the current
		time to get the expiration time. Default to None

	Returns:
		datetime: The calculated expiration time

	Raises:
		ValueError: If expires_delta is invalid or minutes is not set
	"""
	if expires_delta:
		return datetime.now(UTC) + expires_delta
	if minutes is not None:
		return datetime.now(UTC) + timedelta(minutes=minutes)
	value_error: ValueError = ValueError(
		"Either 'expires_delta' or 'minutes' must be provided."
	)
	logger.warning(value_error)
	raise value_error


def create_access_token(
	token_payload: TokenPayload,
	auth_settings: Annotated[AuthSettings, Depends(get_auth_settings)],
	scope: TokenType = TokenType.ACCESS_TOKEN,
	expires_delta: timedelta | None = None,
) -> str:
	"""
	Create a new JWT access token

	Args:
		token_payload (TokenPayload): The payload or claims for the token
		auth_settings (AuthSettings): Dependency method for cached auth setting object
		scope (TokenType): The token's scope. Default to TokenType.ACCESS_TOKEN
		expires_delta (timedelta | None): The timedelta specifying when the token should expire. Default to None

	Returns:
		str: The encoded JWT

	Raises:
		JoseError: If JWT token is invalid
	"""
	payload: dict[str, Any]
	if expires_delta:
		expire_time: datetime = _generate_expiration_time(
			expires_delta, auth_settings.ACCESS_TOKEN_EXPIRE_MINUTES
		)
		updated_payload: TokenPayload = token_payload.model_copy(
			update={"exp": int(expire_time.timestamp()), "scope": scope},
		)
		payload = jsonable_encoder(updated_payload)
	else:
		payload = jsonable_encoder(token_payload)
	header: dict[str, str] = {"alg": auth_settings.ALGORITHM}
	try:
		encoded_jwt: str = jwt.encode(header, payload, auth_settings.SECRET_KEY)
	except JoseError as exc:
		logger.error(f"JWT encoding error: {exc}")
		raise
	logger.info("JWT created with JTI: %s", token_payload.jti)
	return encoded_jwt


def create_refresh_token(
	token_payload: TokenPayload,
	auth_settings: Annotated[AuthSettings, Depends(get_auth_settings)],
) -> str:
	"""
	Create a refresh token for authentication

	Args:
		token_payload (TokenPayload): The data to be used as payload in the token
		auth_settings (AuthSettings): Dependency method for cached auth setting object

	Returns:
		str: The access token with refresh expiration time
	"""
	expires: timedelta = timedelta(
		minutes=auth_settings.REFRESH_TOKEN_EXPIRE_MINUTES,
	)
	token: str = create_access_token(
		token_payload=token_payload,
		auth_settings=auth_settings,
		scope=TokenType.REFRESH_TOKEN,
		expires_delta=expires,
	)
	return token
