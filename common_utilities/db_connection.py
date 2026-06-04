from sqlalchemy import create_engine
from test_configuration.etlTestConfig import *
from test_configuration.logger_config import setup_logger
#DB connection
logger = setup_logger("dbconnection","others.log")
try:
    mysql_engine = create_engine(f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
    oracle_engine = create_engine(f'oracle+oracledb://{ORACLE_USER}:{ORACLE_PASSWORD}@localhost:{ORACLE_PORT}/?service_name={ORACLE_SERVICE}')
except Exception as e:
    logger.error("Error in db connection ",e,exc_info=True)