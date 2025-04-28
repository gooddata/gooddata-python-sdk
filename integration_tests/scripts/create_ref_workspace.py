# (C) 2024 GoodData Corporation
import os
import sys

import pytest
from dotenv import load_dotenv
from workspace_manager import createWorkspace, update_env_file

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(SCRIPTS_DIR)


# Load environment variables from the .env file
load_dotenv()

# Create the test_config dictionary with the loaded environment variables
test_config = {"host": os.getenv("HOST"), "token": os.getenv("TOKEN")}
workspace_id = os.getenv("WORKSPACE_ID")
dataSource_id = os.getenv("DATASOURCE_ID")


def test_create_workspace():
    global workspace_id
    if workspace_id:
        print(f"Workspace ID '{workspace_id}' already exists. Skipping workspace creation.")
    else:
        print("Creating a new workspace...")
        workspace_id = createWorkspace(test_config)
        # dataSource_schema = getDataSource(dataSource_id, test_config)
        # print(f"DataSource schema: {dataSource_schema}")

        if workspace_id:
            update_env_file(workspace_id)
        else:
            print("Failed to create workspace.")
    # updateWorkSpaceLayout(test_config, workspace_id)


if __name__ == "__main__":
    pytest.main()
