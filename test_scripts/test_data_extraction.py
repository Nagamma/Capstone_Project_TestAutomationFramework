import inspect

import pandas as pd
import pytest

from common_utilities.utilities import *

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
        verify_source_to_stage_data(self, file_type="json", file_path="test_data/supplier_data.json", stage_db_engine=get_mysql_database_connection, stage_query=query_actual,test_case_name=test_case_name)
        self.logger.info(f"{test_case_name} test ended......")
        self.logger.info("..................................................................................")



    def test_compare_inventory_xml_and_stage_inventory_data(self,get_mysql_database_connection):
        test_case_name = inspect.currentframe().f_code.co_name
        self.logger.info(f"{test_case_name} test started....")
        query_actual = """select * from stag_inventory"""
        verify_source_to_stage_data(self, file_type="xml", file_path="test_data/inventory_data.xml", stage_db_engine=get_mysql_database_connection, stage_query=query_actual,test_case_name=test_case_name)
        self.logger.info(f"{test_case_name} test ended......")
        self.logger.info("..................................................................................")


