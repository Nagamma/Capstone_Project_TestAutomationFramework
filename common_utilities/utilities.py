from io import StringIO
import paramiko
import pandas as pd
import pytest
import pytest_check as check
import boto3



def verify_source_file_to_stage_db_data(self,file_type,file_path,stage_db_engine,stage_query,test_case_name):
    try:
        if file_type == "csv":
            df_expected = pd.read_csv(file_path)
        elif file_type == "json":
            df_expected = pd.read_json(file_path)
        elif file_type == "xml":
            df_expected = pd.read_xml(file_path,parser="etree",xpath=".//item")
        else:
            raise ValueError(f"File type {file_type} is not supported")

        df_actual = pd.read_sql(stage_query,stage_db_engine)
        # self.logger.info(f"Expected data from file is : {df_expected}")
        #self.logger.info(f"Actual data from database is : {df_actual}")

        validate_expected_vs_actual_data(self, df_expected, df_actual, test_case_name)

    except Exception as e:
        self.logger.error(f"Test Case {test_case_name} execution has failed due to error :{e}", exc_info=True)
        pytest.fail(f"Test execution failed :{e}")



def verify_source_amazon_s3_bucket_file_to_stage_db_data(self,bucket_file_type,bucket_name,file_key,stage_db_engine,stage_query,test_case_name):
    try:
        s3 = boto3.client("s3")
        response = s3.get_object(Bucket=bucket_name, Key=file_key)
        if bucket_file_type == 'csv':
            content = response["Body"].read().decode("utf-8")
            df_expected = pd.read_csv(StringIO(content))
        elif bucket_file_type == 'json':
            content = response["Body"].read().decode("utf-8")
            df_expected = pd.read_json(StringIO(content))
        elif bucket_file_type == 'xml':
            content = response["Body"].read()
            df_expected = pd.read_xml(StringIO(content),parser="etree",xpath=".//item")
        else:
            raise ValueError(f"File type {bucket_file_type} is not supported")

        df_actual = pd.read_sql(stage_query, stage_db_engine)
        validate_expected_vs_actual_data(self, df_expected, df_actual, test_case_name)
    except Exception as e:
        self.logger.error(f"Test Case {test_case_name} execution has failed due to error :{e}", exc_info=True)
        pytest.fail(f"Test execution failed :{e}")

def verify_source_db_data_to_stage_db_data(self,source_db_engine,stage_db_engine,query_expected,query_actual,test_case_name):
    try:
        df_expected = pd.read_sql(query_expected,source_db_engine)
        df_actual = pd.read_sql(query_actual,stage_db_engine)
        validate_expected_vs_actual_data(self,df_expected, df_actual, test_case_name)
    except Exception as e:
        self.logger.error(f"Test Case {test_case_name} execution has failed due to error :{e}", exc_info=True)
        pytest.fail(f"Test execution failed :{e}")

def verify_linux_server_file_to_stage_db_data(self,linux_host,linux_user,linux_password,remote_file_path,local_file_path,stage_db_engine,query_actual,test_case_name):
    try:
        self.logger.info("product file download from linux server has started...")
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=linux_host,username=linux_user,password=linux_password,port=22)
        sftp = ssh_client.open_sftp()
        sftp.get(remote_file_path,local_file_path)
        sftp.close()
        self.logger.info("product file download from linux server has finished...")
        verify_source_file_to_stage_db_data(self, file_type="csv", file_path="test_data/product_data_from_linux.csv", stage_db_engine=stage_db_engine, stage_query=query_actual,test_case_name=test_case_name)
    except Exception as e:
        self.logger.error(f"Test Case {test_case_name} execution has failed due to error :{e}", exc_info=True)
        pytest.fail(f"Test execution failed :{e}")

def validate_expected_vs_actual_data(self,df_expected,df_actual,test_case_name):
    # TestCase-1:Row count validation
    expected_count = len(df_expected)
    actual_count = len(df_actual)
    check.is_true(expected_count == actual_count, "Source and stage data count do not match")

    # TestCase-2: Validate Missing Data (Extra record at expected data)
    missing_records = df_expected[~df_expected.apply(tuple, axis=1).isin(df_actual.apply(tuple, axis=1))]
    # Create CSV if records are missing
    if not missing_records.empty:
        self.logger.info(f"missing records : {missing_records}")
        missing_records.to_csv(f"Differences/missing_records_{test_case_name}.csv", index=False)
    check.is_true(len(missing_records) == 0, "some expected records are missing in db")

    # TestCase-3: Validate extra records in DB (Extra/non matching records at actual data)
    extra_records = df_actual[~df_actual.apply(tuple, axis=1).isin(df_expected.apply(tuple, axis=1))]
    # Create CSV if records are extra
    if not extra_records.empty:
        self.logger.info(f"extra records : {extra_records}")
        extra_records.to_csv(f"Differences/extra_records_{test_case_name}.csv", index=False)
    check.is_true(len(extra_records) == 0,
                  f"some extra records are found at db\n check differences in Differences/extra_records_{test_case_name}.csv file ")

