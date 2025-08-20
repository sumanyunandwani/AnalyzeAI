# Test suite for CustomLogger class
import unittest
import logging
import os
import tempfile
import shutil
from core.custom_logger import CustomLogger

class TestCustomLogger(unittest.TestCase):
    """
    Test suite for CustomLogger class.

    Args:
        unittest.TestCase: Base class for test cases.
    """

    def setUp(self):
        # Temporary directory for logs
        self.test_dir = tempfile.mkdtemp()
        self.logs_dir = os.path.join(self.test_dir, 'logs')

    def tearDown(self):
        # Close all handlers so files are released
        for logger_name in list(logging.Logger.manager.loggerDict.keys()):
            logger = logging.getLogger(logger_name)
            for handler in logger.handlers[:]:
                handler.close()
                logger.removeHandler(handler)

        # Cleanup temp directory
        shutil.rmtree(self.test_dir)

    def test_logger_creation_and_handlers(self):
        """
        Test if the logger is created with file and console handlers.
        """
        logger = CustomLogger.setup_logger('test_logger', logs_dir=self.logs_dir)

        self.assertIsInstance(logger, logging.Logger)

        file_handlers = [h for h in logger.handlers if isinstance(h, logging.FileHandler)]
        console_handlers = [h for h in logger.handlers if isinstance(h, logging.StreamHandler)]

        self.assertTrue(file_handlers, "Logger should have a FileHandler")
        self.assertTrue(console_handlers, "Logger should have a ConsoleHandler")

    def test_sqlalchemy_logger_configured(self):
        """
        Test if SQLAlchemy logger is configured with file and console handlers.
        """
        CustomLogger.setup_logger('test_logger', logs_dir=self.logs_dir)

        sqlalchemy_logger = logging.getLogger("sqlalchemy.engine")
        file_handlers = [
            h for h in sqlalchemy_logger.handlers if isinstance(h, logging.FileHandler)]
        console_handlers = [
            h for h in sqlalchemy_logger.handlers if isinstance(h, logging.StreamHandler)]

        self.assertTrue(file_handlers, "SQLAlchemy logger should have a FileHandler")
        self.assertTrue(console_handlers, "SQLAlchemy logger should have a ConsoleHandler")

    def test_logger_prevents_duplicate_handlers(self):
        """
        Test that the logger does not create duplicate handlers when called multiple times.
        """
        logger1 = CustomLogger.setup_logger('duplicate_logger', logs_dir=self.logs_dir)
        num_handlers = len(logger1.handlers)

        logger2 = CustomLogger.setup_logger('duplicate_logger', logs_dir=self.logs_dir)
        self.assertEqual(
            len(logger2.handlers), num_handlers, "Logger should not duplicate handlers")

    def test_logger_log_file_created(self):
        """
        Test if a log file is created in the specified logs directory.
        """
        CustomLogger.setup_logger('file_creation_logger', logs_dir=self.logs_dir)
        log_files = [f for f in os.listdir(self.logs_dir) if f.endswith('.log')]
        self.assertTrue(log_files, "Log file should be created in logs directory")

    def test_logger_level_is_debug(self):
        """
        Test if the logger's level is set to DEBUG.
        """
        logger = CustomLogger.setup_logger('level_logger', logs_dir=self.logs_dir)
        self.assertEqual(logger.level, logging.DEBUG)


if __name__ == '__main__':
    unittest.main()
