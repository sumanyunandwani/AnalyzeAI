"""
This module defines the SQLs class,
which represents a sqls entity in the database.
"""
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from models.base import Base

class SQLs(Base):
    """
    Represents a SQL file associated with a user.

    Args:
        Base (declarative_base): The base class for declarative models in SQLAlchemy.
    """
    __tablename__ = "sqls"
    sql_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    script_file_path = Column(String, nullable=False)
    business_id = Column(Integer, nullable=False)
    created_on = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
