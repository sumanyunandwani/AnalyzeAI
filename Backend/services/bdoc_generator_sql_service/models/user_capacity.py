"""
This module defines the UserCapacity class,
which represents a user_capacity entity in the database.
"""
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from models.base import Base

class UserCapacity(Base):
    """
    Represents the capacity of a user in terms of SQL and PDF files.

    Args:
        Base (declarative_base): The base class for declarative models in SQLAlchemy.
    """
    __tablename__ = "user_capacity"
    user_id = Column(String, primary_key=True, index=True)
    capacity = Column(Integer, nullable=False, default=4)
    created_on = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
