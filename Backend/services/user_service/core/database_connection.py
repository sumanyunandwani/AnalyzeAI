"""
This file contains the AsyncSQLAlchemySingleton class for managing
an asynchronous SQLAlchemy database connection.
It provides methods to initialize the database engine, create a session,
and create the schema if it does not exist.
"""
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import ProgrammingError
from sqlalchemy import select
from models.base import Base
from models.user import Users

class AsyncSQLAlchemySingleton:
    """
    Singleton class for managing an asynchronous SQLAlchemy database connection.
    Usage:
        db = AsyncSQLAlchemySingleton()
        db.init_engine("postgresql+asyncpg://user:pass@localhost/db")
        async with db.get_session() as session:
            # Perform database operations
    """
    _instance = None
    _engine = None
    _db_url: str = os.getenv("DATABASE_URL")
    _session_local = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def init_engine(self):
        """
        Initializes the SQLAlchemy engine and session factory.

        Args:
            db_url (str): The database URL for the SQLAlchemy engine.
        """
        if not self._engine:
            self._engine = create_async_engine(self._db_url, echo=False, future=True)
            self._session_local = sessionmaker(
                bind=self._engine,
                class_=AsyncSession,
                expire_on_commit=False,
            )

    def get_session(self) -> AsyncSession:
        """
        Provides an asynchronous session for database operations.

        Returns:
            AsyncSession: An instance of AsyncSession for database operations.
        """
        return self._session_local()

    async def create_schema_if_not_exists(self):
        """
        Creates the database schema if it does not already exist.
        This method checks for the existence of the 'users' table
        and creates all tables if it does not exist.
        """
        try:
            async with self._engine.begin() as conn:
                await conn.execute(select(Users))
        except ProgrammingError:
            # If the table does not exist, create all tables
            async with self._engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
# Usage:
# db = AsyncSQLAlchemySingleton()
# db.init_engine("postgresql+asyncpg://user:pass@localhost/db")
# async with db.get_session() as session:
#     ...
