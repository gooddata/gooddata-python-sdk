# (C) 2024 GoodData Corporation
from env import HOST, TOKEN
from workspace_manager import deleteWorkspace

if __name__ == "__main__":
    test_config = {"host": HOST, "token": TOKEN}

    deleteWorkspace(test_config)
