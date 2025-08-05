"""
A module for email tasks in the app.tasks.email tasks package.
"""

import logging
from pathlib import Path
from typing import Annotated

from fastapi import Depends
from pydantic import AnyHttpUrl, EmailStr

from app.config.auth_settings import AuthSettings
from app.config.config import get_auth_settings, get_init_settings, get_settings
from app.config.init_settings import InitSettings
from app.config.settings import Settings
from app.tasks.email_tasks.notification import send_email
from app.tasks.email_tasks.template import (
	read_css_file,
	read_template_file,
	render_template,
)

logger: logging.Logger = logging.getLogger(__name__)


def build_email_template(
	template_file: str,
	css_file: str,
	init_settings: Annotated[InitSettings, Depends(get_init_settings)],
) -> tuple[str, str]:
	"""
	Builds the email template and CSS

	Args:
		template_file (str): The template file
		css_file (str): The CSS file
		init_settings (InitSettings): Dependency method for cached init setting object

	Returns:
		tuple[str, str]: The template and CSS read as strings
	"""
	template_path: Path = (
		init_settings.EMAIL_TEMPLATES_DIR.resolve() / template_file
	)
	css_path: Path = init_settings.CSS_DIRECTORY.resolve() / css_file
	template_str: str = read_template_file(template_path, init_settings)
	css_str: str = read_css_file(css_path, init_settings)
	return template_str, css_str


def send_new_account_confirmation_email(
	email_to: EmailStr,
	name: str,
	message: str,
	settings: Annotated[Settings, Depends(get_settings)],
	auth_settings: Annotated[AuthSettings, Depends(get_auth_settings)],
	init_settings: Annotated[InitSettings, Depends(get_init_settings)],
) -> None:
	"""
	Send a new account confirmation email

	Args:
		email_to (EmailStr): The email address of the recipient
		name (str): Name of the recipient
		message (str): Message from the recipient
		settings (Settings): Dependency method for cached setting object
		auth_settings (AuthSettings): Dependency method for cached auth setting object
		init_settings (InitSettings): Dependency method for cached init setting object

	Returns:
		NoneType: None
	"""
	template_str, css_str = build_email_template(
		"new_account.html", "styles.css", init_settings
	)
	url: AnyHttpUrl = auth_settings.WEBSITE_URL
	html_content: str = render_template(
		template_str,
		css_str,
		{
			"name": name,
			"email": email_to,
			"message": message,
			"link": f"{url}",
		},
	)
	sent_email: bool | str = send_email(
		email_to=email_to,
		subject=settings.EMAIL_SUBJECT,
		html_content=html_content,
		settings=settings,
		init_settings=init_settings,
	)
	logger.info(sent_email)
