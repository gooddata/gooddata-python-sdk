# (C) 2024 GoodData Corporation
import json
import os
import time
import uuid
from datetime import datetime
from pathlib import Path

from gooddata_sdk import CatalogDeclarativeWorkspaces, CatalogWorkspace, GoodDataSdk

_current_dir = Path(__file__).parent.absolute()
_fixtures_dir = _current_dir / "fixtures"


def createWorkspace(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])

    workspace_id = uuid.uuid4().hex
    timestamp = datetime.utcnow().isoformat()
    workspace_name = f"python_sdk_test_{int(time.time())} -- {timestamp}"

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
        print("Attempting to delete workspaces...")
        workspaces = sdk.catalog_workspace.list_workspaces()
        for workspace in workspaces:
            if workspace.name.startswith("python_sdk_test_"):
                sdk.catalog_workspace.delete_workspace(workspace.id)
                print(f"Workspace '{workspace.name}' with ID '{workspace.id}' deleted successfully.")
        remove_env_file()
    except Exception as e:
        print(f"An error occurred while deleting workspaces: {e}")


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


def updateWorkSpaceLayout(test_config, workspaceId):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    # dataSourceSchema= getDataSource(dataSourceId, test_config)

    with open(_fixtures_dir / "demo_load_and_put_declarative_workspaces.yaml") as f:
        data = json.load(f)
        workspaces_e = CatalogDeclarativeWorkspaces.from_dict(data)

    # try:
    sdk.catalog_workspace.put_declarative_workspace(
        workspace_id=workspaceId, CatalogDeclarativeWorkspaceModel=workspaces_e
    )
    workspace_o = sdk.catalog_workspace.get_declarative_workspaces(workspace_id=workspaceId, exclude=["ACTIVITY_INFO"])
    assert workspaces_e == workspace_o
    assert workspaces_e.to_dict(camel_case=True) == workspace_o.to_dict(camel_case=True)
