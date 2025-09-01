"""
This module defines the DBService class to manage database operations
related to user capacity, IPs, SQL scripts, PDFs, and requests.
It provides methods to get counts for users and IPs, update counts,
insert new records, and retrieve specific data from the database.
"""
from typing import Optional
from logging import Logger
from sqlalchemy import select, update
from core.custom_logger import CustomLogger
from core.database_connection import AsyncSQLAlchemySingleton
from models.ips import IPs
from models.user_capacity import UserCapacity
from models.sql import SQLs
from models.pdf import PDFs
from models.requests import Requests
from models.business import Businesses

class DBService:
    """
    Count Service class offers count values.
    Usage:
        count_service_obj = CountService(db_connection, jwt_auth)
        count_for_user = count_service_obj.get_count_for_user(token)
        count_for_ip = count_service_obj.get_count_for_ip(ip_address)
    """
    def __init__(self,
                db_connection: AsyncSQLAlchemySingleton,
                logger: Optional[Logger] = CustomLogger.setup_logger(__name__)
            ):
        self._db = db_connection
        self.logger = logger

    async def get_count_for_user(self, user_id: str) -> Optional[int]:
        """
        Returns Number of Requests Left for User

        Args:
            token (dict): JWT Token contianing user info

        Returns:
            int: Number of Requests Left
        """
        async with self._db.get_session() as session:
            sql_stmt = select(UserCapacity.capacity).where(UserCapacity.user_id == user_id)
            result = await session.execute(sql_stmt)
        return result.scalar_one_or_none()

    async def get_count_for_ip(self, ip_address: str) -> Optional[int]:
        """
        Returns Number of Requests Left for that IP

        Args:
            ip_address (str): IP address for the user

        Returns:
            int: Number of Requests Left
        """
        async with self._db.get_session() as session:
            sql_stmt = select(IPs.count).where(IPs.ip_address == ip_address)
            result = await session.execute(sql_stmt)
        return result.scalar_one_or_none()

    async def update_count_for_user(self, user_id: str, new_count: int) -> bool:
        """
        Updating Count for User

        Args:
            user_id (str): Combination of Name and Email
            new_count (int): Number of Requests Remaining

        Returns:
            bool: True for Success, False for Failure
        """
        async with self._db.get_session() as session:
            sql_stmt = (
                update(UserCapacity)
                .where(UserCapacity.user_id == user_id)
                .values(capacity=new_count)
            )
            result = await session.execute(sql_stmt)
            await session.commit()
        return result.rowcount > 0

    async def update_count_for_ip(self, ip_address: str, new_count: int) -> bool:
        """
        Updating Count for IP

        Args:
            ip_address (str): IP Address of User
            new_count (int): Number of Requests Remaining

        Returns:
            bool: True for Success, False for Failure
        """
        async with self._db.get_session() as session:
            sql_stmt = (
                update(IPs)
                .where(IPs.ip_address == ip_address)
                .values(count=new_count)
            )
            result = await session.execute(sql_stmt)
            await session.commit()
        return result.rowcount > 0

    async def inset_new_ip(self, ip_address: str) -> int:
        """
        Inserts a new record for the given IP address into the database.
        This method creates a new IPs entry with the provided IP address
        and commits it to the database asynchronously.

        Args:
            ip_address (str): The IP address to be inserted into the database.

        Raises:
            Exception: If there is an error during database insertion or commit.

        Returns:
            int: The count of requests left for the newly inserted IP address.
        """
        async with self._db.get_session() as session:
            new_ip = IPs(ip_address=ip_address)
            session.add(new_ip)
            await session.commit()
            await session.refresh(new_ip)
        return new_ip.count

    async def insert_new_user(self, user_id: str) -> int:
        """
        Inserts a new user record into the UserCapacity table.

        Args:
            user_id (str): The unique identifier for the user.

        Returns:
            int: The initial capacity for the newly inserted user.
        """
        async with self._db.get_session() as session:
            new_user = UserCapacity(
                user_id=user_id
            )
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)
        return new_user.capacity

    async def insert_sql_script(self, sql_script_path: str, business_id: int) -> int:
        """
        Inserts a new SQL script into the SQLs table.
        Args:
            sql_script (str): The SQL script to be inserted.
            business_id (int): The ID of the business associated with the SQL script.
        Returns:
            int: The ID of the newly inserted SQL script record.
        """
        async with self._db.get_session() as session:
            new_sql = SQLs(
                script_file_path=sql_script_path,
                business_id=business_id
            )
            session.add(new_sql)
            await session.commit()
            await session.refresh(new_sql)
        return new_sql.sql_id

    async def insert_pdf_file(self, file_path: str, sql_id: int) -> int:
        """
        Inserts a new PDF file record into the PDFs table.

        Args:
            file_path (str): The file path of the PDF.
            sql_id (int): The ID of the associated SQL script.
        Returns:
            int: The ID of the newly inserted PDF record.
        """
        async with self._db.get_session() as session:
            new_pdf = PDFs(
                file_path=file_path,
                sql_id=sql_id
            )
            session.add(new_pdf)
            await session.commit()
            await session.refresh(new_pdf)
        return new_pdf.pdf_id

    async def insert_new_request(
            self,
            request_id: str,
            user_id: str = None,
            ip_address: str = None,
            pdf_id: int = None) -> bool:
        """
        Inserts a new request record into the Requests table.

        Args:
            request_id (str): The unique identifier for the request.
            user_id (str, optional): The ID of the user making the request.
            ip_address (str, optional): The IP address of the user making the request.
            pdf_id (int, optional): The ID of the associated PDF file.
        
        Returns:
            bool: Returns True if the insertion and commit were successful.
        """
        async with self._db.get_session() as session:
            sql_stmt = Requests(
                request_id=request_id,
                pdf_id=pdf_id,
                user_id=user_id,
                ip_address=ip_address
            )
            session.add(sql_stmt)
            await session.commit()
        return True

    async def get_business_id_from_business_name(self, business_name: str) -> Optional[int]:
        """
        Retrieves the business ID from the business name.

        Args:
            business_name (str): The name of the business.
        Returns:
            Optional[int]: The ID of the business if found, otherwise None.
        """
        async with self._db.get_session() as session:
            sql_stmt = select(Businesses.business_id).where(
                Businesses.name == business_name
            )
            result = await session.execute(sql_stmt)
        return result.scalar_one_or_none()

    async def get_request_by_request_id(self, request_id: str) -> Optional[Requests]:
        """
        Retrieves a request record by its request ID.

        Args:
            request_id (str): The unique identifier for the request.
        
        Returns:
            Optional[Requests]: The request record if found, otherwise None.
        """
        async with self._db.get_session() as session:
            sql_stmt = select(Requests).where(Requests.request_id == request_id)
            result = await session.execute(sql_stmt)
        return result.scalar_one_or_none()

    async def get_pdf_file_path_by_pdf_id(self, pdf_id: int) -> Optional[str]:
        """
        Retrieves the file path of a PDF by its ID.

        Args:
            pdf_id (int): The ID of the PDF file.
        Returns:
            Optional[str]: The file path of the PDF if found, otherwise None.
        """
        async with self._db.get_session() as session:
            sql_stmt = select(PDFs.file_path).where(PDFs.pdf_id == pdf_id)
            result = await session.execute(sql_stmt)
        return result.scalar_one_or_none()

    async def get_all_business(self) -> list[str]:
        """
        Retrieves all the business names in the DB

        Returns:
            list[str]: List of business name in DB
        """
        async with self._db.get_session() as session:
            sql_stmt = select(Businesses.name)
            result = await session.execute(sql_stmt)
        return result.scalars().all()
