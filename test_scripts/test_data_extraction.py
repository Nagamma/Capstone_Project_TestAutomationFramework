import pandas as pd
import pytest

@pytest.mark.usefixtures("get_mysql_database_connection","get_logger")
class TestDataExtraction:
    def test_compare_supplier_json_and_stage_supplier_data(self,get_mysql_database_connection,get_logger):
        logger = get_logger("extraction_logger", "extraction.log")
        logger.info("Supplier data comparison test started")
        try:
            df_expected = pd.read_json('test_data/supplier_data.json')
            query_actual = """select * from stag_suplier"""
            df_actual = pd.read_sql(query_actual,get_mysql_database_connection)
            assert df_actual.equals(df_expected),"Supplier data did not extract correctly"
            logger.info("Test Passed: Supplier JSON data matched with stage_supplier table data")
        except Exception as e:
            logger.error(f"Test failed due to error :{e}",exc_info=True)
            pytest.fail(f"Test execution failed :{e}")

    def test_compare_inventory_xml_and_stage_inventory_data(self,get_mysql_database_connection,get_logger):
        logger = get_logger("extraction_logger", "extraction.log")
        logger.info(f"Inventory data comparison test started")
        try:
            df_expected = pd.read_xml('test_data/inventory_data.xml',parser='etree',xpath=".//item")
            query_actual = """select * from stag_inventory"""
            df_actual = pd.read_sql(query_actual,get_mysql_database_connection)
            assert df_actual.equals(df_expected), "Inventory data did not extract correctly"
            logger.info("Test Passed: Inventory data matched with stage_inventory table data")
        except Exception as e:
            logger.error(f"Test failed due to error :{e}",exc_info=True)
            pytest.fail(f"Test execution failed :{e}")

