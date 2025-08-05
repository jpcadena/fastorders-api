"""
A module for template in the app.tasks.email tasks package.
"""

import logging
from typing import Annotated, Any

from fastapi import Depends
from jinja2 import Template
from pydantic import FilePath

from app.config.config import get_init_settings
from app.config.init_settings import InitSettings

logger: logging.Logger = logging.getLogger(__name__)


def render_template(
	template: str,
	css: str | None,
	environment: dict[str, Any],
) -> str:
	"""
	Renders the given template with the given environment variables and inlines
	CSS.

	Args:
		template (str): The body of the email in HTML format
		css (str | None): The CSS css as a string
		environment (dict[str, Any]): A dictionary of variables used in the email templates

	Returns:
		str: Rendered template with environment variables and inline CSS
	"""
	rendered_html: str = Template(template).render(environment)
	logger.info("Rendered HTML")
	if not css:
		return rendered_html
	html_with_css: str = rendered_html.replace(
		'<link href="/assets/css/css.css" rel="stylesheet" />',
		f"<style>\n{css}\n\t</style>",
	)
	logger.info("HTML with CSS added")
	return html_with_css


def read_template_file(
	template_path: FilePath,
	init_settings: Annotated[InitSettings, Depends(get_init_settings)],
) -> str:
	"""
	Read the template file

	Args:
		template_path (FilePath): Path to the template
		init_settings (InitSettings): Dependency method for cached init setting object

	Returns:
		str: Template string
	"""
	with open(template_path, encoding=init_settings.ENCODING) as file:
		template: str = file.read()
	return template


def read_css_file(
	css_path: FilePath,
	init_settings: Annotated[InitSettings, Depends(get_init_settings)],
) -> str:
	"""
	Read the CSS file

	Args:
		css_path (FilePath): Path to the CSS file
		init_settings (InitSettings): Dependency method for cached init setting object

	Returns:
		str: CSS string
	"""
	with open(css_path, encoding=init_settings.ENCODING) as file:
		css_lines: list[str] = file.readlines()
	indented_css: str = "".join(["\t  " + line for line in css_lines])
	return indented_css
