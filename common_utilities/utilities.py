import pandas as pd
import pytest
import pytest_check as check

def verify_source_to_stage_data(self,file_type,file_path,stage_db_engine,stage_query,test_case_name):
    try:
        if file_type == "csv":
            df_expected = pd.read_csv(file_path)
        elif file_type == "json":
            df_expected = pd.read_json(file_path)
        elif file_type == "xml":
            df_expected = pd.read_xml(file_path,parser="etree",xpath=".//item")
        else:
            raise ValueError(f"File type {file_type} is not supported")
        #self.logger.info(f"Expected data from file is : {df_expected}")
        df_actual = pd.read_sql(stage_query,stage_db_engine)
        #self.logger.info(f"Actual data from database is : {df_actual}")

        #TestCase-1:Row count validation
        expected_count = len(df_expected)
        actual_count = len(df_actual)
        #assert expected_count == actual_count, "Source and stage data count do not match"
        check.is_true(expected_count == actual_count,"Source and stage data count do not match")
        #self.logger.info(f"Row Count Validation Passed: expected_count : {expected_count} and actual count is : {actual_count}")

        #TestCase-2:Full Data Comparision (Not Recommended)
        # assert df_actual.equals(df_expected), "Source and stage data do not match"
        # self.logger.info("Full Data Comparision Test Passed: expected data matched with actual data")

        #TestCase-2: Validate Missing Data (Extra record at expected data)
        missing_records = df_expected[~df_expected.apply(tuple,axis=1).isin(df_actual.apply(tuple,axis=1))]
        # Create CSV if records are missing
        if not missing_records.empty:
            self.logger.info(f"missing records : {missing_records}")
            missing_records.to_csv(f"Differences/missing_records_{test_case_name}.csv",index=False)

        #assert len(missing_records) == 0, "some expected records are missing in db"
        check.is_true(len(missing_records) == 0, "some expected records are missing in db")
        #self.logger.info("There are no missing records in db")

        #TestCase-3: Validate extra records in DB (Extra/non matching records at actual data)
        extra_records = df_actual[~df_actual.apply(tuple,axis=1).isin(df_expected.apply(tuple,axis=1))]
        #Create CSV if records are extra
        if not extra_records.empty:
            self.logger.info(f"extra records : {extra_records}")
            extra_records.to_csv(f"Differences/extra_records_{test_case_name}.csv",index=False)
        #assert len(extra_records) == 0, "some extra records are found at db"
        check.is_true(len(extra_records) == 0, "some extra records are missing in db")
        #self.logger.info("There are no extra records in db")
    except Exception as e:
        self.logger.error(f"Test Case {test_case_name} execution has failed due to error :{e}", exc_info=True)
        pytest.fail(f"Test execution failed :{e}")
