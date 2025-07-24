"""
Package app.models.structured initialization.
"""

from app.models.base_class import Base
from app.models.structured.order import Order
from app.models.structured.order_item import OrderItem
from app.models.structured.product import Product
from app.models.structured.user import User

__all__: list[Base] = [User, Product, Order, OrderItem]
