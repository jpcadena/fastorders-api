"""
A module for api in the app.api.api v1 package.
"""

from fastapi import APIRouter

from app.api.api_v1.router import order, order_item, product, user

api_router: APIRouter = APIRouter()
api_router.include_router(user.router)
api_router.include_router(order.router)
api_router.include_router(product.router)
api_router.include_router(order_item.router)
