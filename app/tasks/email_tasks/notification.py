"""
A module for notification in the app.tasks.email tasks package.
"""

import logging
from email.mime.multipart import MIMEMultipart
from typing import Annotated

from fastapi import Depends
from pydantic import EmailStr

from app.config.config import get_init_settings, get_settings
from app.config.init_settings import InitSettings
from app.config.settings import Settings
from app.tasks.email_tasks.message import create_message, send_email_message

logger: logging.Logger = logging.getLogger(__name__)


def send_email(
	email_to: EmailStr,
	subject: str,
	html_content: str,
	settings: Annotated[Settings, Depends(get_settings)],
	init_settings: Annotated[InitSettings, Depends(get_init_settings)],
) -> bool | str:
	"""
	Send an e-mail to a recipient.

	Args:
		email_to (EmailStr): The email address of the recipient
		subject (str): The subject of the email
		html_content (str): The body of the email in HTML format
		settings (Settings): Dependency method for cached setting object
		init_settings (InitSettings): Dependency method for cached init setting object

	Returns:
		bool | str: True if the email was sent; otherwise an error message
	"""
	message: MIMEMultipart = create_message(
		email_to,
		subject,
		html_content,
		settings,
	)
	is_sent: bool | str = send_email_message(
		message,
		settings,
		init_settings.ENCODING,
	)
	return is_sent
