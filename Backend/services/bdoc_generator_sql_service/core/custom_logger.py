"""
Custom logger setup with file and console handlers, including SQLAlchemy engine logging.
"""
import logging
import os
import datetime

class CustomLogger:
    """
    Custom Logger class to set up logging with file and console handlers.
    """
    @staticmethod
    def setup_logger(name: str, logs_dir: str = None) -> logging.Logger:
        """
        Set up a logger with file + console handlers.
        Also configures SQLAlchemy engine logger to use the same handlers.

        Args:
            name (str): Logger name.
            logs_dir (str, optional): Directory to store log files.

        Returns:
            logging.Logger: Configured logger instance.
        """
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        # Prevent duplicate handlers
        if logger.handlers:
            return logger

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # Default logs directory
        if logs_dir is None:
            logs_dir = os.path.join(
                os.path.dirname(
                    os.path.dirname(__file__)
                ), 'logs')

        # Ensure logs directory exists
        os.makedirs(logs_dir, exist_ok=True)

        # File handler
        log_file_name = f"{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
        file_path = os.path.join(logs_dir, log_file_name)
        file_handler = logging.FileHandler(file_path)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # Configure SQLAlchemy logger
        sqlalchemy_logger = logging.getLogger("sqlalchemy.engine")
        sqlalchemy_logger.setLevel(logging.INFO)
        sqlalchemy_logger.addHandler(file_handler)
        sqlalchemy_logger.addHandler(console_handler)

        return logger
