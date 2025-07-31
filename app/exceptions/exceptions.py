"""
This module defines custom exception classes for the Core Security
"""

from fastapi import HTTPException, status


class ServiceException(HTTPException):
	"""Service Layer Exception class"""

	def __init__(self, message: str, note: str | None = None):
		super().__init__(status.HTTP_503_SERVICE_UNAVAILABLE, message)
		if note:
			self.add_note(note)


class SecurityException(HTTPException):
	"""Security Exception class"""

	def __init__(self, message: str, note: str | None = None):
		super().__init__(
			status.HTTP_511_NETWORK_AUTHENTICATION_REQUIRED, message
		)
		if note:
			self.add_note(note)
