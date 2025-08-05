"""
A module for message in the app.tasks.email tasks package.
"""

import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Annotated

import resend
from fastapi import Depends, HTTPException, status
from pydantic import EmailStr
from resend.exceptions import ResendError

from app.config.config import get_settings
from app.config.settings import Settings

logger: logging.Logger = logging.getLogger(__name__)


def create_message(
	email_to: EmailStr,
	subject: str,
	html: str,
	settings: Annotated[Settings, Depends(get_settings)],
) -> MIMEMultipart:
	"""
	Creates an email message with the given HTML content and subject

	Args:
		email_to (EmailStr): The email address of the recipient
		subject (str): The subject of the email
		html (str): Rendered template with environment variables
		settings (Settings): Dependency method for cached setting object

	Returns:
		MIMEMultipart: Message with subject and rendered template
	"""
	mime_multipart: MIMEMultipart = MIMEMultipart("alternative")
	mime_multipart["Subject"] = subject
	mime_multipart["From"] = (
		f"{settings.EMAILS_FROM_NAME} <{settings.EMAILS_FROM_EMAIL}>"
	)
	mime_multipart["To"] = email_to
	mime_text: MIMEText = MIMEText(html, "html")
	mime_multipart.attach(mime_text)
	logger.info("Message created from: %s", settings.EMAILS_FROM_EMAIL)
	return mime_multipart


def send_email_message(
	message: MIMEMultipart,
	settings: Annotated[Settings, Depends(get_settings)],
	encoding: str,
) -> bool | str:
	"""
	Sends the message to the given email address.

	Args:
		message (MIMEMultipart): The email message
		settings (Settings): Dependency method for cached setting object
		encoding (str): Encoding of the file.

	Returns:
		bool | str: True if the email was sent; otherwise an error message
	"""
	try:
		resend.api_key = settings.RESEND_API_KEY
		html_content: str | None = None
		payload_reference: bytes
		for part in message.walk():
			if part.get_content_type() == "text/html":
				payload_reference = part.get_payload(  # type: ignore
					decode=True
				)
				html_content = payload_reference.decode(encoding)
		if not html_content:
			raise HTTPException(
				status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
				detail="HTML content is missing.",
			)
		params: resend.Emails.SendParams = {
			"from": message["From"],
			"to": message["To"],
			"subject": message["Subject"],
			"html": html_content,
		}
		email: resend.Email = resend.Emails.send(params)
		logger.info("Sent email %s to %s", email["id"], message["to"])
		return True
	except ResendError as exc:
		error_msg = f"Unexpected error sending email to {message['To']}: {exc}"
		logger.error(error_msg)
		return error_msg
	except Exception as e:
		logger.error(f"An unexpected error occurred: {e}")
		return str(e)
