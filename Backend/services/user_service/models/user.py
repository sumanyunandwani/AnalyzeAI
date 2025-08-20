"""
This module defines the Users model for the user service.
It includes fields for user_id, name, email, subscription status,
and the creation timestamp.
Subscription is an integer that defaults to 0, indicating no active subscription.
1 means a subscription is active of type 1.
2 means a subscription is active of type 2.
"""
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from .base import Base


class Users(Base):
    """
    Represents a user in the database.

    Args:
        Base (declarative_base): The base class for declarative models in SQLAlchemy.
    """
    __tablename__ = "users"
    user_id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=True)
    subscription = Column(Integer, default=0, nullable=False)
    created_on = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
