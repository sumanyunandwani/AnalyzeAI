"""
This module defines the Businesses class,
which represents a business entity in the database.
"""
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from models.base import Base

class Businesses(Base):
    """
    Represents a business entity in the database.

    Args:
        Base (declarative_base): The base class for declarative models in SQLAlchemy.
    """
    __tablename__ = "businesses"
    business_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    created_on = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
