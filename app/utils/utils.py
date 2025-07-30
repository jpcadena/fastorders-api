"""
A module for utils in the app.utils package.
"""

import logging
import re

from app.exceptions.exceptions import ServiceException

logger: logging.Logger = logging.getLogger(__name__)


def validate_password(password: str | None) -> str:
	"""
	Validates a password based on given criteria.

	Args:
		password (str | None): The password to validate

	Returns:
		str: The validated password
	"""
	msg: str
	if not password:
		msg = "Password cannot be empty or None"
		logger.exception(msg)
		raise ServiceException("Password cannot be empty or None")
	if not (
		re.search("[A-Z]", password)
		and re.search("[a-z]", password)
		and re.search("[0-9]", password)
		and re.search("[#?!@$%^&*-]", password)
		and 8 <= len(password) <= 14
	):
		msg = "Password validation failed"
		logger.error(msg)
		raise ValueError("Password validation failed")
	return password
