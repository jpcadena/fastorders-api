"""
A module for token type in the app.core.enums package.
"""

from enum import UNIQUE, StrEnum, auto, verify


@verify(UNIQUE)
class TokenType(StrEnum):
	"""Enum representing different types of tokens."""

	ACCESS_TOKEN = auto()
	REFRESH_TOKEN = auto()
