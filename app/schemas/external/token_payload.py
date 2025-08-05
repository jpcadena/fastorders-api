"""
A module for token payload in the app.schemas.external package.
"""

from app.schemas.external.claims.public_claims_token import PublicClaimsToken
from app.schemas.external.claims.registered_claims_token import (
	RegisteredClaimsToken,
)


class TokenPayload(PublicClaimsToken, RegisteredClaimsToken):
	"""
	Token Payload class based on RegisteredClaimsToken and PublicClaimsToken.
	"""
