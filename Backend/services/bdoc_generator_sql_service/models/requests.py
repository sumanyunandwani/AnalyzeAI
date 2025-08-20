"""
This module defines the Requests class,
which represents a requests entity in the database.
"""
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from models.base import Base

class Requests(Base):
    """
    Represents a request made by a user.

    Args:
        Base (declarative_base): The base class for declarative models in SQLAlchemy.
    """
    __tablename__ = "requests"
    request_id = Column(String, primary_key=True, index=True, nullable=False)
    user_id = Column(Integer, nullable=True)
    pdf_id = Column(Integer, nullable=False)
    ip_address = Column(String, nullable=True)
    created_on = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
