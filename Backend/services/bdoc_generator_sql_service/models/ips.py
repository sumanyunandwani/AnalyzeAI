"""
This module defines the IPs class,
which represents a ips entity in the database.
"""
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from models.base import Base

class IPs(Base):
    """
    Represents an IP address associated with a user.

    Args:
        Base (declarative_base): The base class for declarative models in SQLAlchemy.
    """
    __tablename__ = "ips"
    ip_address = Column(String, primary_key=True, nullable=False)
    count = Column(Integer, nullable=False, default=3)
    created_on = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
