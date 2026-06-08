import logging
import os
import pytest

from sqlalchemy import create_engine
from test_configuration.etlTestConfig import *

@pytest.fixture
def get_logger():
    #fixture factory (fixture returning a function).
    def _get_logger(logger_name,log_file):
        logger = logging.getLogger(logger_name)
        # Prevent duplicate handlers
        if logger.hasHandlers():
            logger.handlers.clear()
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler = logging.FileHandler(os.path.join('logs',log_file),mode='a')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        return logger
    return _get_logger

@pytest.fixture
def get_mysql_database_connection(get_logger):
    logger = get_logger("db_logger","database.log")
    logger.info('Connecting to MySQL database...')
    try:
        mysql_engine = create_engine(f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}').connect()
        logger.info('MySQL database connected.')
        yield mysql_engine
        mysql_engine.close()
        logger.info('MySQL database closed.')
    except Exception as e:
        logger.error("Error in db connection ", e, exc_info=True)

@pytest.fixture
def get_oracle_database_connection(get_logger):
    logger = get_logger("db_logger", "database.log")
    logger.info('Connecting to Oracle database...')
    try:
        oracle_engine = create_engine(f'oracle+oracledb://{ORACLE_USER}:{ORACLE_PASSWORD}@localhost:{ORACLE_PORT}/?service_name={ORACLE_SERVICE}').connect()
        logger.info('Oracle database connected.')
        yield oracle_engine
        oracle_engine.close()
        logger.info('Oracle database closed.')
    except Exception as e:
        logger.error("Error in db connection ", e, exc_info=True)