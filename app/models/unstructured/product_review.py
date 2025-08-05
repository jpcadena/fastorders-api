"""
A module for product review in the app.models.unstructured package.
"""

from datetime import datetime, timedelta
from uuid import UUID, uuid4

from beanie import Document, Insert, Replace, Update, before_event
from pydantic import Field, PositiveInt, constr
from pydantic_extra_types.coordinate import Coordinate
from pydantic_extra_types.country import CountryAlpha2
from pydantic_extra_types.currency_code import Currency


class ProductReview(Document):
	"""Product Review document for MongoDB collection"""

	product_id: UUID = Field(
		default_factory=uuid4, description="ID of the reviewed product"
	)
	user_id: UUID = Field(
		default_factory=uuid4, description="ID of the user who made the review"
	)
	rating: PositiveInt = Field(
		..., ge=1, le=5, description="Rating from 1 to 5"
	)
	title: constr(strip_whitespace=True, max_length=100) = Field(...)
	comment: constr(strip_whitespace=True, max_length=1000) = Field(...)
	country: CountryAlpha2 | None = Field(None, description="Reviewer country")
	currency: Currency | None = Field(
		None, description="Currency of transaction"
	)
	geo_location: Coordinate | None = Field(
		None, description="Approx user location"
	)
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

		name = "product_reviews"
		use_cache = True
		cache_expiration_time = timedelta(seconds=10)
		cache_capacity = 5
		validate_on_save = True
