"""
A module for init settings in the app.config package.
"""

from pathlib import Path

from pydantic import DirectoryPath
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.utils.image_utils import convert_image_to_base64


class InitSettings(BaseSettings):
	"""Init Settings class based on Pydantic Base Settings"""

	model_config = SettingsConfigDict(
		case_sensitive=True,
		extra="allow",
	)

	ASSETS_APP: str = "assets"
	ASSETS_DIR: str = f"/{ASSETS_APP}"
	STATIC_DIR: str = "static"
	TEMPLATES_DIR: str = "static/templates"
	IMAGES_SUBDIR: str = "images"
	CSS_SUBDIR: str = "css"
	IMAGES_DIRECTORY: DirectoryPath = Path(ASSETS_APP) / IMAGES_SUBDIR
	CSS_DIRECTORY: DirectoryPath = Path(STATIC_DIR) / CSS_SUBDIR
	API_NAME: str = "Fast Orders API"
	PROJECT_NAME: str = "fastorders-api"
	VERSION: str = "1.0"
	ENCODING: str = "UTF-8"
	OPENAPI_FILE_PATH: str = "/openapi.json"
	DATETIME_FORMAT: str = "%Y-%m-%d %H:%M:%S"
	FILE_DATE_FORMAT: str = "%d-%b-%Y-%H-%M-%S"
	EMAIL_TEMPLATES_DIR: DirectoryPath = Path(TEMPLATES_DIR)
	LOG_FORMAT: str = (
		"[%(name)s][%(asctime)s][%(levelname)s][%(module)s]"
		"[%(funcName)s][%(lineno)d]: %(message)s"
	)
	SUMMARY: str = """
	This backend project is a RESTful API developed with FastAPI. This project
	serves as the backend to manager orders along with users
	"""
	img_b64: str = convert_image_to_base64(
		IMAGES_DIRECTORY.resolve() / "project.png"
	)
	DESCRIPTION: str = f"""
	**FastAPI**, **SQLAlchemy** and **MemCached** helps you do awesome stuff.
	🚀\n\n<img src="{img_b64}" width="1000px" height="500px"/>
	"""
	LICENSE_INFO: dict[str, str] = {
		"name": "MIT",
		"identifier": "MIT",
	}
