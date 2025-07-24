"""
A module for base class in the app.models package.
"""

from sqlalchemy.orm import declarative_base
from sqlalchemy.orm.decl_api import DeclarativeMeta

Base: type[DeclarativeMeta] = declarative_base()
