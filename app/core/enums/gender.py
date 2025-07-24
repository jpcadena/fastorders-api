"""
A module for gender in the app.core.enums package.
"""

from enum import UNIQUE, StrEnum, auto, verify


@verify(UNIQUE)
class Gender(StrEnum):
	"""Enum representing different gender options"""

	MALE = auto()
	FEMALE = auto()
	OTHER = auto()
