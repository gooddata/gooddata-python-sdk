# (C) 2024 GoodData Corporation
import os
import sys
import time
import uuid

from gooddata_sdk import CatalogWorkspace, GoodDataSdk

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from env import WORKSPACE_ID
except ImportError:
    WORKSPACE_ID = None


def createWorkspace(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])

    workspace_id = uuid.uuid4().hex
    timestamp = int(time.time())
    workspace_name = f"pysdk_test_{timestamp}"

    workspace = CatalogWorkspace(workspace_id, workspace_name)
    try:
        sdk.catalog_workspace.create_or_update(workspace)
        workspace_o = sdk.catalog_workspace.get_workspace(workspace_id)
        assert workspace_o == workspace

        print(f"Workspace '{workspace_name}' with ID '{workspace_id}' created successfully.")
        return workspace_id
    except Exception as e:
        print(f"An error occurred while creating the workspace: {e}")
        return None


def deleteWorkspace(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    try:
        workspaces = sdk.catalog_workspace.list_workspaces()
        for workspace in workspaces:
            if workspace.name.startswith("pysdk_test_"):
                sdk.catalog_workspace.delete_workspace(workspace.id)
                print(f"Workspace '{workspace.name}' with ID '{workspace.id}' deleted successfully.")
        remove_env_file()
    except Exception as e:
        print(f"An error occurred while deleting workspaces: {e}")


def update_env_file(workspace_id):
    with open("env.py", "a") as f:
        f.write(f'\nWORKSPACE_ID = "{workspace_id}"\n')


def remove_env_file():
    try:
        with open("env.py") as f:  # Default mode is 'r'
            lines = f.readlines()
        with open("env.py", "w") as f:
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
