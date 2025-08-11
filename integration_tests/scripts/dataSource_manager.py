# (C) 2024 GoodData Corporation
import os
import time
import uuid
from datetime import datetime

from gooddata_sdk import BasicCredentials, CatalogDataSourceSnowflake, GoodDataSdk, SnowflakeAttributes


def createDataSource(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    dataSourceId = uuid.uuid4().hex
    timestamp = datetime.utcnow().isoformat()
    dataSourceName = f"python_sdk_test_ds_{int(time.time())} -- {timestamp}"
    data_source = (
        CatalogDataSourceSnowflake(
            id=dataSourceId,
            name=dataSourceName,
            db_specific_attributes=SnowflakeAttributes(account="gooddata", warehouse="TIGER_PERF", db_name="CHECKLIST"),
            schema="demo",
            credentials=BasicCredentials(username="qa01_test", password=os.getenv("DATASOURCE_PASSWORD")),
        ),
    )
    print(f"Creating a new dataSource: ${data_source}")
    try:
        sdk.catalog_data_source.create_or_update_data_source(data_source)
        dataSource_o = sdk.catalog_data_source.get_data_source(dataSourceId)

        print(f"DataSource '{dataSource_o}'")
        assert dataSource_o == data_source

        print(f"DataSource '{dataSourceName}' with ID '{dataSourceId}' created successfully.")
        return dataSourceId
    except Exception as e:
        print(f"An error occurred while creating the dataSource: {e}")
        return None


def deleteDataSource(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    try:
        print("Attempting to delete dataSource...")
        dataSources = sdk.catalog_data_source.list_data_sources()
        for dataSource in dataSources:
            if dataSource.attributes.name.startswith("python_sdk_test_ds_"):
                sdk.catalog_data_source.delete_data_source(dataSource.id)
                print(f"dataSource '{dataSource.attributes.name}' with ID '{dataSource.id}' deleted successfully.")
        remove_env_file()
    except Exception as e:
        print(f"An error occurred while deleting dataSource: {e}")


def update_env_file(workspace_id):
    env_file_path = os.path.join(os.path.dirname(__file__), "..", ".env")
    print(f"Updating env.py with WORKSPACE_ID: {workspace_id} into ${env_file_path}")
    with open(env_file_path, "a") as f:
        f.write(f'\nWORKSPACE_ID = "{workspace_id}"\n')


def remove_env_file():
    env_file_path = os.path.join(os.path.dirname(__file__), "..", ".env")
    try:
        with open(env_file_path) as f:  # Default mode is 'r'
            lines = f.readlines()
        with open(env_file_path, "w") as f:
            for line in lines:
                if "WORKSPACE_ID" not in line:
                    f.write(line)
        print("Removed WORKSPACE_ID from env.py")
    except Exception as e:
        print(f"An error occurred while removing WORKSPACE_ID from env.py: {e}")


def getDataSource(data_source_id, test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    data_source = sdk.catalog_data_source.get_data_source(data_source_id)
    data_source_schema = data_source.schema
    print(f"Data source schema: {data_source_schema}")
    return data_source_schema
