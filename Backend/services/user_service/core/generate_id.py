"""
This module provides a utility class for generating unique user identifiers.
The GenerateUserId class creates a SHA-256 hash based on a user's name and email,
ensuring consistent and unique IDs for each user. If the email is missing,
a default placeholder is used. This is useful for systems that require
anonymized or consistent user identification.
"""
import hashlib
from typing import Optional
from logging import Logger
from sqlalchemy.dialects.postgresql import insert
from core.custom_logger import CustomLogger
from core.database_connection import AsyncSQLAlchemySingleton
from models.user import Users

class GenerateId:
    """
    GenerateUserId is a utility class for generating consistent and unique user identifiers.
    This class provides methods to create a hash-based user ID
    from a combination of user name and email.
    It ensures that the generated ID is unique for each distinct name-email pair,
    and handles cases where
    the email may be missing by substituting a default value.
    Typical usage:
        generator = GenerateUserId()
        user_id = generator.generate_user_id("Alice", "alice@example.com")
    """
    def __init__(self, logger: Optional[Logger] = None):
        """
        Initializes the GenerateId class with an optional logger.

        Args:
            logger (Optional[Logger]): An instance of a logger for logging messages.
        """
        self.logger = logger or CustomLogger.setup_logger(__name__)

    def generate_user_id(self, name: str, email: Optional[str]) -> str:
        """
        Generates a consistent and unique hash for a name and email combination

        Args:
            name (str): Name of User
            email (str): Email of User

        Returns:
            str: Hash Combination of both
        """
        email = email or "not_found@not_found.com"
        combined = f"{name.lower().strip()}|{email.lower().strip()}"
        return hashlib.sha256(combined.encode("utf-8")).hexdigest()

    async def create_user(
            self,
            name: str,
            email: Optional[str],
            db_connection: AsyncSQLAlchemySingleton
        ) -> bool:
        """
        Creates a new user in the database with the generated user ID.

        Args:
            name (str): Name of the user.
            email (Optional[str]): Email of the user, can be None.
            db_connection (AsyncSQLAlchemySingleton): Database connection instance.
        Returns:
            bool: True if user creation is successful, False otherwise.
        """
        user_id = self.generate_user_id(name, email)

        async with db_connection.get_session() as session:
            new_user = insert(Users).values(
                user_id=user_id,
                name=name,
                email=email or "not_found@not_found.com"
            ).on_conflict_do_update(
                index_elements=["user_id"],
                set_={
                    "name": name,
                    "email": email or "not_found@not_found.com"
                }
            )

            await session.execute(new_user)
            await session.commit()

        self.logger.info(f"User created with ID: {user_id}")

        return True
