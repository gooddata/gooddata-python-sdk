# (C) 2024 GoodData Corporation
import os

# import sys
import pytest
from dotenv import load_dotenv
from workspace_manager import deleteWorkspace

# SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
# sys.path.append(SCRIPTS_DIR)


load_dotenv()

test_config = {"host": os.getenv("HOST"), "token": os.getenv("TOKEN")}


def test_delete_workspace():
    deleteWorkspace(test_config)


if __name__ == "__main__":
    pytest.main(["-s", __file__])
