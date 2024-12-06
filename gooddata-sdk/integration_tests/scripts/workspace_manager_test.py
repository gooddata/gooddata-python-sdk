# (C) 2024 GoodData Corporation
# import pytest
# from workspace_manager import create_workspace, delete_workspace, get_data_source, update_env_file
# from env import DATASOURCE_ID, HOST, TOKEN
# @pytest.fixture
# def test_config():
#     return {
#         'host': HOST,
#         'token': TOKEN
#     }

# def test_create_workspace(test_config):
#     workspace_id = create_workspace(test_config)
#     assert workspace_id is not None, "Workspace creation failed"
#     update_env_file(workspace_id)

# # def test_delete_workspace(test_config):
# #     delete_workspace(test_config)
# #     # Assuming the function prints the deletion message, we can check the output
# #     # Here we assume that the function works correctly if no exception is raised

# def test_get_data_source(test_config):
#     schema = get_data_source(DATASOURCE_ID, test_config)
#     assert schema is not None, "Failed to get data source schema"

# if __name__ == "__main__":
#     pytest.main()
