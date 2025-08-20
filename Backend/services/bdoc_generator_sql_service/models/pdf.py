"""
This module defines the PDFs class,
which represents a pdfs entity in the database.
"""
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from models.base import Base

class PDFs(Base):
    """
    Represents a PDF file associated with a user.

    Args:
        Base (declarative_base): The base class for declarative models in SQLAlchemy.
    """
    __tablename__ = "pdfs"
    pdf_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    file_path = Column(String, nullable=False)
    sql_id = Column(Integer, nullable=False)
    created_on = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
