import inspect

import pandas as pd
import pytest

from common_utilities.utilities import *
from test_configuration.etlTestConfig import *

@pytest.mark.usefixtures("get_mysql_database_connection","get_logger")
class TestDataExtraction:
    #Run this fixture automatically for every test without explicitly calling it.
    @pytest.fixture(autouse=True)
    def setup(self,get_logger):
        self.logger = get_logger("extraction_logger", "extraction.log")

    def test_compare_supplier_json_and_stage_supplier_data(self,get_mysql_database_connection):
        test_case_name = inspect.currentframe().f_code.co_name
        self.logger.info(f"{test_case_name} test started.....")
        query_actual = """select * from stag_suplier"""
        verify_source_file_to_stage_db_data(self, file_type="json", file_path="test_data/supplier_data.json", stage_db_engine=get_mysql_database_connection, stage_query=query_actual,test_case_name=test_case_name)
        self.logger.info(f"{test_case_name} test ended......")
        self.logger.info("..................................................................................")

    def test_compare_inventory_xml_and_stage_inventory_data(self,get_mysql_database_connection):
        test_case_name = inspect.currentframe().f_code.co_name
        self.logger.info(f"{test_case_name} test started....")
        query_actual = """select * from stag_inventory"""
        verify_source_file_to_stage_db_data(self, file_type="xml", file_path="test_data/inventory_data.xml", stage_db_engine=get_mysql_database_connection, stage_query=query_actual,test_case_name=test_case_name)
        self.logger.info(f"{test_case_name} test ended......")
        self.logger.info("..................................................................................")

    def test_compare_sales_s3_bucket_and_stage_sales_data(self,get_mysql_database_connection):
        test_case_name = inspect.currentframe().f_code.co_name
        self.logger.info(f"{test_case_name} test started....")
        query_actual = """select * from stag_sales"""
        verify_source_amazon_s3_bucket_file_to_stage_db_data(self,bucket_file_type='csv',bucket_name=S3_BUCKET_NAME,file_key=FILE_KEY,stage_db_engine=get_mysql_database_connection,stage_query=query_actual,test_case_name=test_case_name)
        self.logger.info(f"{test_case_name} test ended......")
        self.logger.info("..................................................................................")

    def test_compare_store_db_and_stage_store_data(self,get_mysql_database_connection,get_oracle_database_connection):
        test_case_name = inspect.currentframe().f_code.co_name
        self.logger.info(f"{test_case_name} test started....")
        query_expected = """select * from stores"""
        query_actual = """select * from stag_stores"""
        source_db_engine = get_oracle_database_connection
        stage_db_engine = get_mysql_database_connection
        verify_source_db_data_to_stage_db_data(self,source_db_engine=source_db_engine,stage_db_engine=stage_db_engine,query_expected=query_expected,query_actual=query_actual,test_case_name=test_case_name)
        self.logger.info(f"{test_case_name} test ended......")
        self.logger.info("..................................................................................")

    def test_compare_linux_server_product_data_and_stage_product_data(self,get_mysql_database_connection):
        test_case_name = inspect.currentframe().f_code.co_name
        self.logger.info(f"{test_case_name} test started....")
        query_actual = """select * from stag_product"""
        verify_linux_server_file_to_stage_db_data(self,linux_host=LINUX_HOST,linux_user=LINUX_USER,linux_password=LINUX_PASSWORD,
                                                  remote_file_path=LINUX_REMOTE_PRODUCT_DATA_FILE_PATH,local_file_path=LOCAL_PRODUCT_DATA_FILE_PATH,
                                                  stage_db_engine=get_mysql_database_connection,query_actual=query_actual,test_case_name=test_case_name)
        self.logger.info(f"{test_case_name} test ended......")
        self.logger.info("..................................................................................")



