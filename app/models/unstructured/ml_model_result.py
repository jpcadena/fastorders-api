"""
A module for ml model result in the app.models.unstructured package.
"""

from datetime import datetime, timedelta
from uuid import UUID, uuid4

from beanie import Document, Insert, Replace, Update, before_event
from pydantic import Field, PositiveFloat
from pydantic_extra_types.coordinate import Coordinate


class MLModelResult(Document):
	"""Output of a Machine Learning model stored for audit or suggestions"""

	user_id: UUID = Field(
		default_factory=uuid4, description="User requesting the prediction"
	)
	session_id: UUID = Field(
		default_factory=uuid4, description="Session ID or traceability"
	)
	model_name: str = Field(..., description="Model used for inference")
	prediction: str = Field(..., description="Text output or label")
	probability: PositiveFloat | None = Field(None, ge=0.0, le=1.0)

	feature_vector: dict[str, float] | None = Field(
		None, description="Optional raw model inputs"
	)
	geo_location: Coordinate | None = None
	created_at: datetime | None = None
	updated_at: datetime | None = None

	@before_event(Insert)
	async def set_created_at(self) -> None:
		"""
		Before database Insert event to set created_at attribute as now

		Returns:
			NoneType: None
		"""
		self.created_at = datetime.now()

	@before_event([Update, Replace])
	async def set_updated_at(self) -> None:
		"""
		Before database Update and Replace events to set updated_at

		Returns:
			NoneType: None
		"""
		self.updated_at = datetime.now()

	class Settings:
		"""Settings for MongoDB collection"""

		name = "ml_model_results"
		use_cache = True
		cache_expiration_time = timedelta(seconds=10)
		cache_capacity = 5
		validate_on_save = True
