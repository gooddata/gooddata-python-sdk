# (C) 2024 GoodData Corporation
from env import DATASOURCE_ID, HOST, TOKEN, WORKSPACE_ID
from workspace_manager import createWorkspace, getDataSource, update_env_file

if __name__ == "__main__":
    test_config = {"host": HOST, "token": TOKEN}

    if WORKSPACE_ID:
        print(f"Workspace ID '{WORKSPACE_ID}' already exists. Skipping workspace creation.")
    else:
        workspace_id = createWorkspace(test_config)
        dataSource = getDataSource(DATASOURCE_ID, test_config)
        if workspace_id:
            update_env_file(workspace_id)
        else:
            print("Failed to create workspace.")
