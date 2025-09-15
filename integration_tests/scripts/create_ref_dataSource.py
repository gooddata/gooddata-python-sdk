# (C) 2024 GoodData Corporation
import os
import sys

import pytest
from dataSource_manager import createDataSource, update_env_file
from dotenv import load_dotenv

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(SCRIPTS_DIR)


# Load environment variables from the .env file
load_dotenv()

# Create the test_config dictionary with the loaded environment variables
test_config = {"host": os.getenv("HOST"), "token": os.getenv("TOKEN")}
dataSourceId = os.getenv("DATASOURCE_ID")


def test_create_data_source():
    global dataSourceId
    if dataSourceId:
        print(f"DataSource ID '{dataSourceId}' already exists. Skipping dataSource creation.")
    else:
        print("Creating a new dataSource...")
        dataSourceId = createDataSource(test_config)
        # dataSource = getDataSource(DATASOURCE_ID, test_config)
        if dataSourceId:
            update_env_file(dataSourceId)
        else:
            print("Failed to create dataSource.")


if __name__ == "__main__":
    pytest.main()
