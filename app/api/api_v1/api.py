"""
A module for api in the app.api.api v1 package.
"""

from fastapi import APIRouter

from app.api.api_v1.router import user

api_router: APIRouter = APIRouter()
api_router.include_router(user.router)
